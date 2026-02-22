from urllib import response
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import sqlite3
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 🔥 RAG IMPORTS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama


# ============================
# CONFIG
# ============================

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ============================
# ENTERPRISE ROLE PERMISSIONS
# ============================

ROLE_PERMISSIONS = {
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General", "C-Level"]
}

# ============================
# VECTOR DB + EMBEDDING
# ============================

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vector_db",
    embedding_function=embedding
)

# ============================
# LOCAL LLM (OLLAMA)
# ============================

llm = Ollama(
    model="llama3",
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)

# ============================
# DATABASE HELPER
# ============================

def init_access_log_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            query TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize table automatically at startup
init_access_log_table()


def log_access(username, role, query, status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO access_logs (username, role, query, status)
        VALUES (?, ?, ?, ?)
    """, (username, role, query, status))
    conn.commit()
    conn.close()


def get_user_from_db(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"username": user[0], "password": user[1], "role": user[2]}
    return None

# ============================
# JWT FUNCTIONS
# ============================

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================
# LOGIN ENDPOINT
# ============================

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_db(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "role": user["role"]
    }


# ============================
# CHAT REQUEST MODEL
# ============================

class ChatRequest(BaseModel):
    query: str


# ============================
# ENTERPRISE RAG CHAT ENDPOINT
# ============================

@app.post("/chat")
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):

    query = request.query
    user_role = current_user["role"]
    username = current_user["username"]

    docs_with_scores = vectordb.similarity_search_with_score(query, k=5)

    SIMILARITY_THRESHOLD = 1.5

    filtered_docs = []

    for doc, score in docs_with_scores:
        if score <= SIMILARITY_THRESHOLD:
            filtered_docs.append(doc)

    if user_role != "C-Level":
        filtered_docs = [
            doc for doc in filtered_docs
            if doc.metadata.get("category") in [user_role, "General"]
        ]

    if not filtered_docs:
        log_access(username, user_role, query, "DENIED")
        return {
            "answer": "🚫 Access Denied or No relevant information found.",
            "confidence": 0,
            "blocked_chunks": 0,
            "sources": []
        }

    filtered_docs = filtered_docs[:3]

    context = "\n\n".join([doc.page_content for doc in filtered_docs])

    prompt = f"""
You are an enterprise AI assistant.
Answer ONLY using the context below.
If the answer is not in the context, say you do not have access.

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    log_access(username, user_role, query, "GRANTED")

    return {
        "answer": response.strip(),
        "confidence": 0.9,
        "blocked_chunks": len(docs_with_scores) - len(filtered_docs),
        "sources": [doc.metadata.get("source") for doc in filtered_docs]
    }


# ============================
# ADMIN-ONLY LOG VIEW ENDPOINT
# ============================

@app.get("/logs")
def view_logs(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "C-Level":
        raise HTTPException(status_code=403, detail="Admin access required")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, role, query, status, timestamp
        FROM access_logs
        ORDER BY timestamp DESC
    """)

    logs = cursor.fetchall()
    conn.close()

    return {"logs": logs}
