from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import sqlite3

from auth import create_access_token, decode_token, verify_password
from access_log import log_access

# ----- LLM -----
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from transformers import pipeline

from rbac_demo import ROLE_ACCESS_MAP

app = FastAPI(title="RBAC Secured LLM Chatbot")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DB_NAME = "users.db"
TOKEN_BLACKLIST = set()

# --------------------------
# LOAD LLM + VECTOR DB ONCE
# --------------------------
embedding = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=200
)

# --------------------------
# Models
# --------------------------
class ChatRequest(BaseModel):
    query: str


# --------------------------
# Database
# --------------------------
def get_user(username: str):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT username, password, role FROM users WHERE username=?",
        (username,)
    )

    user = cur.fetchone()
    conn.close()
    return user


# --------------------------
# Auth
# --------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in TOKEN_BLACKLIST:
        raise HTTPException(status_code=401, detail="Token revoked")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


# --------------------------
# Routes
# --------------------------

@app.get("/")
def root():
    return {"status": "API running"}


# -------- LOGIN --------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------- LOGOUT --------
@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    TOKEN_BLACKLIST.add(token)
    return {"message": "Logged out successfully"}


# -------- CHAT --------
@app.post("/chat")
def chat(data: ChatRequest, user=Depends(get_current_user)):

    username = user["sub"]
    role = user["role"]          # keep case as-is
    query = data.query

    # 1️⃣ Vector search
    retrieved_docs = vectordb.similarity_search(query, k=5)

    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="No documents found")

    # 2️⃣ RBAC filtering (DOCUMENT BASED)
    allowed_tags = ROLE_ACCESS_MAP.get(role, [])

    authorized_docs = [
        doc for doc in retrieved_docs
        if doc.metadata.get("tag") in allowed_tags
    ]

    # 3️⃣ Enforce RBAC
    if not authorized_docs:
        log_access(username, role, query, "DENIED")
        raise HTTPException(
            status_code=403,
            detail="Access denied by RBAC"
        )

    # 4️⃣ Build context ONLY from authorized docs
    context = "\n\n".join(doc.page_content for doc in authorized_docs)
    context = context[:2000]

    # 5️⃣ LLM Prompt
    prompt = f"""
Answer ONLY using the context below.

Context:
{context}

Question:
{query}
"""

    response = llm(prompt)[0]["generated_text"]

    log_access(username, role, query, "GRANTED")

    return {
        "user": username,
        "role": role,
        "answer": response
    }

