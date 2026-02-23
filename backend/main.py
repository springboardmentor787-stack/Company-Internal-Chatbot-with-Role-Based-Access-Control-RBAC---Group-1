from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from backend.auth import authenticate_user, create_access_token, verify_token
from backend.rag import rag_pipeline
from backend.audit import log_access

app = FastAPI(title="Company Internal Chatbot Backend")

security = HTTPBearer()


# =========================
# Request Models
# =========================

class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    question: str


# =========================
# Root Endpoint
# =========================

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}


# =========================
# LOGIN ENDPOINT
# =========================

@app.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": token}


# =========================
# JWT Validation Dependency
# =========================

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
    
@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "username": user["sub"],
        "role": user["role"]
    }


# =========================
# CHAT ENDPOINT (RAG + RBAC)
# =========================

@app.post("/chat")
def chat(data: ChatRequest, user=Depends(get_current_user)):

    role = user["role"]
    username = user["sub"]

    # 🔹 Call RAG pipeline
    result = rag_pipeline(
        query=data.question,
        user_role=role
    )

    answer = result["answer"]
    sources = result["sources"]
    confidence = result["confidence"]
    status = result.get("status", "OK")

    # 🔹 If invalid role
    if status == "Invalid role":
        log_access(username, role, "N/A", "Invalid role")
        raise HTTPException(status_code=403, detail="Invalid role")

    # 🔹 Log access
    log_access(username, role, "auto", status)

    return {
        "user": username,
        "role": role,
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }
