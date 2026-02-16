from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.database import SessionLocal
from backend.models import User
from backend.auth.jwtHandler import create_access_token
from backend.auth.dependencies import get_current_user
from backend.auth.rbac import require_roles
from backend.auth.audit import log_access
from backend.rag.pipeline import run_rag
from fastapi import Request, HTTPException, Depends
from backend.auth.rbac import require_roles
#from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.auth.audit import log_access
from langchain_chroma import Chroma
from fastapi import Depends
#from backend.auth.jwt_handler import get_current_user

app = FastAPI(title="RBAC Chatbot")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Health Check ----------------
@app.get("/")
def health():
    return {"message": "Backend is running successfully"}

# @app.get("/me")
# def get_current_user(current_user: User = Depends(get_current_user)):
#     return {
#         "username": current_user.username,
#         "role": current_user.role,
#         "dept": current_user.dept
#     }


# ---------------- LOGIN ----------------
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
        # "department": user.dept
    }


# ---------------- Protected Example ----------------
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "username": current_user.username,
        "role": current_user.role
    }


# ---------------- HR ----------------
@app.get("/hr-data")
def hr_data(user=Depends(require_roles(["HR", "C-Level"]))):
    log_access(user.username, user.role, "/hr-data", "ALLOWED")
    return {"message": "HR confidential data"}


# ---------------- Finance ----------------
@app.get("/finance-data")
def finance_data(user=Depends(require_roles(["Finance", "C-Level"]))):
    log_access(user.username, user.role, "/finance-data", "ALLOWED")
    return {"message": "Finance confidential data"}


# ---------------- Marketing ----------------
@app.get("/marketing-data")
def marketing_data(user=Depends(require_roles(["Marketing", "C-Level"]))):
    log_access(user.username, user.role, "/marketing-data", "ALLOWED")
    return {"message": "Marketing confidential data"}


# ---------------- Engineering ----------------
@app.get("/engineering-data")
def engineering_data(user=Depends(require_roles(["Engineering", "C-Level"]))):
    log_access(user.username, user.role, "/engineering-data", "ALLOWED")
    return {"message": "Engineering internal data"}


# ---------------- General ----------------
@app.get("/general")
def general_data(user=Depends(get_current_user)):
    log_access(user.username, user.role, "/general", "ALLOWED")
    return {"message": "General company information"}


#------------------ RAG Endpoint ------------------

@app.post("/rag-chunks")
def rag_chunks(
    payload: dict,
    request: Request,
    user = Depends(require_roles(
        ["Finance", "HR", "Engineering", "Marketing", "C-Level"]
    ))
):
    # ================= Validate Query =================
    query = payload.get("query")

    if not query or not isinstance(query, str) or not query.strip():
        raise HTTPException(status_code=400, detail="Query is required")

    query = query.strip()

    # ================= Retrieve Documents =================
    try:
        results = vector_db.similarity_search_with_score(query, k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector DB error: {str(e)}")

    visible_chunks = []
    blocked_count = 0
    allowed_scores = []

    # ================= RBAC Filtering =================
    for doc, score in results:

        # Safe metadata extraction
        metadata = doc.metadata or {}
        allowed_roles = metadata.get("allowed_roles", []) or []

        chunk_info = {
            "source": metadata.get("source"),
            "dept": metadata.get("dept"),
            "allowed_roles": allowed_roles,
            "content": doc.page_content
        }

        # Role-based filtering
        if user.role == "C-Level" or user.role in allowed_roles:
            visible_chunks.append(chunk_info)
            allowed_scores.append(score)
        else:
            blocked_count += 1

    # ================= Confidence Calculation =================
    if allowed_scores:
        avg_distance = sum(allowed_scores) / len(allowed_scores)
        confidence = round(1 / (1 + avg_distance), 3)
    else:
        confidence = 0.0

    # ================= Response =================
    return {
        "query": query,
        "user_role": user.role,
        "username": user.username,
        "retrieved_chunks": len(results),
        "allowed_chunks": visible_chunks,
        "blocked_chunks_count": blocked_count,
        "confidence": confidence,
        
    }
# ================= Audit Logging =================
#     log_access(
#        user=user,
#        endpoint=request.url.path,
#        query=query,
#        status="ALLOWED" if visible_chunks else "NO_ACCESS"
#   )