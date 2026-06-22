from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from backend.db import (
    get_user,
    verify_password,
    insert_log,
    get_all_logs,
    get_stats
)

from backend.search import role_based_search
from backend.rag import generate_answer

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    role = payload.get("role")
    return {"username": username, "role": role}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or not verify_password(form_data.password, user["password"]):
        return {"error": "Invalid credentials"}

    access_token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": access_token, "token_type": "bearer"}


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(req: ChatRequest, user=Depends(get_current_user)):

    results = role_based_search(req.query, user["role"], user["username"])

    if not results:
        insert_log(user["username"], user["role"], req.query, "DENIED")
        return {"answer": "Access denied or no relevant documents found."}

    chunks = [doc.page_content for doc in results]

    answer = generate_answer(req.query, chunks)

    insert_log(user["username"], user["role"], req.query, "ALLOWED")

    return {"answer": answer}


@app.get("/admin/logs")
def admin_logs(user=Depends(get_current_user)):
    if user["role"] != "C-Level":
        return {"error": "Not authorized"}

    return {"logs": get_all_logs()}


@app.get("/admin/stats")
def admin_stats(user=Depends(get_current_user)):
    if user["role"] != "C-Level":
        return {"error": "Not authorized"}

    total, role_counts = get_stats()

    return {
        "total_queries": total,
        "queries_per_role": role_counts
    }