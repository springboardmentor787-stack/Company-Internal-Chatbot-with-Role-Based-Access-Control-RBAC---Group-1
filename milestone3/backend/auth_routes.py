from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt
from backend.logger import get_logger
logger = get_logger("auth")


SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

USERS = {
    "finance1": {"password": "password123", "role": "Finance"},
    "hr1": {"password": "password123", "role": "HR"},
    "engineer1": {"password": "password123", "role": "Engineering"},
    "ceo1": {"password": "password123", "role": "C-Level"},
}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login attempt username={form.username}")

    user = USERS.get(form.username)
    if not user or user["password"] != form.password:
        logger.warning(f"Failed login username={form.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"Login success username={form.username} role={user['role']}")

    token = jwt.encode(
        {"sub": form.username, "role": user["role"]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}
