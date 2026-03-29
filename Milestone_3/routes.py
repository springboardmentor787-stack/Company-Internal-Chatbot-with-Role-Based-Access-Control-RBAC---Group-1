from fastapi import Depends, HTTPException, APIRouter, Query
from fastapi.security import OAuth2PasswordRequestForm
import sqlite3
import time

from milestone_3.database import DB_PATH
from milestone_3.models import verify_password, hash_password
from milestone_3.auth import create_access_token, get_current_user
from milestone_3.rbac import rbac_required
from milestone_3.logs import log_access
from milestone_3.rag import rag_pipeline
from milestone_3.search_service import search_with_rbac

router = APIRouter()


# ================= LOGIN =================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password, role FROM users WHERE username=?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_username, db_password, role = user

    if not verify_password(password, db_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_username,
        "role": role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ================= GET CURRENT USER =================
@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/secure-search")
def secure_search(
    department: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    start_time = time.time()

    role = current_user["role"].lower()
    username = current_user["username"]

    # Strict department match (except C-Level)
    if role != "c-level" and role != department.lower():
        raise HTTPException(
            status_code=403,
            detail="Access denied for this department"
        )

    # 🔎 Fetch real documents
    results = search_with_rbac(
        query=f"{department} department data",
        user_role=role
    )

    # Filter strictly by department
    department_docs = [
        {
            "source": r["source"],
            "department": r["department"],
            
        }
        for r in results
        if r["department"].lower() == department.lower()
    ]

    end_time = time.time()
    response_time = round(end_time - start_time, 2)

    log_access(
        username=username,
        role=role,
        query=f"/secure-search?department={department}",
        confidence=100.0 if department_docs else 0.0,
        response_time=response_time
    )

    return {
        "requested_department": department,
        "access_granted_for_role": role,
        "documents": department_docs,
        "total_documents": len(department_docs),
        "response_time": response_time
    }


# ================= ADMIN PANEL ROUTES =================

# ---- VIEW ALL USERS ----
@router.get("/admin/users")
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"].lower() != "c-level":
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return [{"username": u[0], "role": u[1]} for u in users]


# ---- ADD NEW USER ----
@router.post("/admin/add-user")
def add_user(
    username: str,
    password: str,
    role: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "c-level":
        raise HTTPException(status_code=403, detail="Access denied")

    role = role.lower()

    allowed_roles = ["engineering", "finance", "hr", "marketing", "employees", "c-level"]

    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_password, role)
    )

    conn.commit()
    conn.close()

    return {"message": "User added successfully"}


# ---- DELETE USER ----
@router.delete("/admin/delete-user")
def delete_user(
    username: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "c-level":
        raise HTTPException(status_code=403, detail="Access denied")

    if username == current_user["username"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user[0].lower() == "c-level":
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='c-level'")
        count = cursor.fetchone()[0]
        if count <= 1:
            conn.close()
            raise HTTPException(status_code=400, detail="Cannot delete last C-Level user")

    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

    return {"message": "User deleted successfully"}


# ================= VIEW CHAT HISTORY =================
@router.get("/history")
def view_history(current_user: dict = Depends(get_current_user)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    role = current_user["role"].lower()
    username = current_user["username"]

    if role == "c-level":
        cursor.execute("""
            SELECT username, role, query, confidence, response_time, timestamp
            FROM access_logs
            ORDER BY timestamp DESC
        """)
    else:
        cursor.execute("""
            SELECT username, role, query, confidence, response_time, timestamp
            FROM access_logs
            WHERE username = ?
            ORDER BY timestamp DESC
        """, (username,))

    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "username": r[0],
            "role": r[1],
            "query": r[2],
            "confidence": r[3],
            "response_time": r[4],
            "timestamp": r[5]
        }
        for r in rows
    ]

    return history