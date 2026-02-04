from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
import sqlite3
from milestone_3.database import DB_PATH
from milestone_3.models import verify_password
from milestone_3.auth import create_access_token, get_current_user
from milestone_3.rbac import rbac_required
from milestone_3.logs import log_access
from milestone_3.rag import rag_pipeline
from pydantic import BaseModel

router = APIRouter()

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

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user


# --------- FINAL RBAC ENDPOINT (CORRECT MODEL) ---------

@router.get("/secure-search")
def secure_search(
    department: str = Query(..., description="finance, hr, engineering, marketing, general"),
    current_user: dict = Depends(get_current_user)
):
    role = current_user["role"]
    username = current_user["username"]

    # RBAC CHECK
    rbac_required(department)(current_user)

    # LOG
    log_access(username, role, f"/secure-search?department={department}", confidence=1.0)

    return {
        "requested_department": department,
        "access_granted_for_role": role,
        "data": f"Confidential {department} data"
    }

# class ChatRequest(BaseModel):
#     query: str

# @router.post("/chat")
# def chat(
#     request: ChatRequest,
#     current_user: dict = Depends(get_current_user)
# ):
#     role = current_user["role"]
#     result = rag_pipeline(request.query, role)
#     return result






















# @router.post("/chat")
# def chat(
#     query: str,
#     current_user: dict = Depends(get_current_user)
# ):
#     role = current_user["role"]
#     username = current_user["username"]

#     result = rag_pipeline(query, role)

#     log_access(username, role, f"/chat → {query}")

#     return result












# no parameter in secure_search
# from fastapi import APIRouter, HTTPException, Depends, Query
# from fastapi.security import OAuth2PasswordRequestForm
# import sqlite3
# from milestone_3.database import DB_PATH
# from milestone_3.models import verify_password
# from milestone_3.auth import create_access_token, get_current_user
# from milestone_3.rbac import rbac_required
# from milestone_3.logs import log_access

# router = APIRouter()

# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT username, password, role FROM users WHERE username=?",
#         (username,)
#     )
#     user = cursor.fetchone()
#     conn.close()

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     db_username, db_password, role = user

#     if not verify_password(password, db_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({
#         "sub": db_username,
#         "role": role
#     })

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }

# @router.get("/me")
# def read_me(current_user: dict = Depends(get_current_user)):
#     return current_user


# # --------- PROTECTED ENDPOINT (FIXED) ---------

# @router.get("/secure-search")
# def secure_search(current_user: dict = Depends(rbac_required())):
#     username = current_user["username"]
#     role = current_user["role"]

#     # LOG HERE (Step 9)
#     log_access(username, role, "/secure-search")

#     role_lower = role.lower()

#     if role_lower == "finance":
#         return {"data": "Finance confidential data"}

#     elif role_lower == "hr":
#         return {"data": "HR confidential data"}

#     elif role_lower == "engineering":
#         return {"data": "Engineering confidential data"}

#     elif role_lower == "marketing":
#         return {"data": "Marketing confidential data"}

#     elif role_lower == "employees":
#         return {"data": "General company data"}

#     elif role_lower == "c-level":
#         return {"data": "All company data"}

#     return {"data": "No data"}
