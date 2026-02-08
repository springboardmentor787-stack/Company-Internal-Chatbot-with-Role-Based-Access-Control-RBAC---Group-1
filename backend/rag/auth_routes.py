from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, User
from jwt_utils import create_access_token
from security import verify_password  # Make sure this is imported

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # 1. Query the database instead of the hardcoded dict
    user = db.query(User).filter(User.username == data.username).first()

    # 2. Verify user exists and password matches hash
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. Create token with role from DB
    token = create_access_token(
        {"sub": user.username, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }