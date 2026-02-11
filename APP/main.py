from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

from .database import init_db, get_user
from .security import verify_password, create_token, decode_token
from .rag import generate_answer
from .logger import log_event

app = FastAPI(title="COMPANY INTERNAL CHATBOT", version="1.0")

# ✅ CORS FIX (Important for Failed to fetch error)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

init_db()


# -----------------------------
# Request Models
# -----------------------------

class ChatRequest(BaseModel):
    department: str = Field(..., example="hr")
    question: str = Field(..., example="What is the sick leave policy?")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    login_time: str


# -----------------------------
# Login Endpoint
# -----------------------------

@app.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = get_user(form_data.username)

    if not user or not verify_password(form_data.password, user[1]):
        return {"error": "Invalid credentials"}

    token = create_token(user[0], user[2])

    return {
        "access_token": token,
        "token_type": "bearer",
        "login_time": datetime.now().isoformat()
    }


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(
    data: ChatRequest,
    token: str = Depends(oauth2_scheme)
):

    try:
        payload = decode_token(token)

        answer, confidence, status = generate_answer(
            data.question,
            payload["role"],
            data.department
        )

        log_event(
            payload["sub"],
            payload["role"],
            data.question,
            answer,
            confidence,
            status
        )

        return {
            "department": data.department,
            "question": data.question,
            "answer": answer,
            "confidence": confidence,
            "status": status
        }

    except Exception as e:
        return {"error": str(e)}
