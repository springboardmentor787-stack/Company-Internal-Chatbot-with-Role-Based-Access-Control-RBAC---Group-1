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

app = FastAPI(title="RBAC Chatbot")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Backend is running successfully"}

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
        data={"sub": user.username, "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "Access granted to protected route",
        "username": current_user.username,
        "role": current_user.role
    }

@app.get("/hr-data")
def hr_data(user=Depends(require_roles(["HR", "C-Level"]))):
    log_access(
        username=user.username,
        role=user.role,
        endpoint="/hr-data",
        action="ALLOWED"
    )
    return {
        "message": "HR confidential data",
        "user": user.username,
        "role": user.role
    }

@app.get("/finance-data")
def finance_data(user=Depends(require_roles(["Finance", "C-Level"]))):
    log_access(
        username=user.username,
        role=user.role,
        endpoint="/finance-data",
        action="ALLOWED"
    )
    return {
        "message": "Finance confidential data",
        "accessed_by": user.username,
        "role": user.role
    }


@app.get("/general")
def general_data(user=Depends(get_current_user)):
    log_access(
        username=user.username,
        role=user.role,
        endpoint="/general",
        action="ALLOWED"
    )
    return {
        "message": "General company information",
        "user": user.username,
        "role": user.role
    }

@app.get("/marketing-data")
def marketing_data(user=Depends(require_roles(["Marketing", "C-Level"]))):
    log_access(
        username=user.username,
        role=user.role,
        endpoint="/marketing-data",
        action="ALLOWED"
    )
    return {
        "message": "Marketing confidential data",
        "accessed_by": user.username,
        "role": user.role
    }

@app.get("/engineering-data")
def engineering_data(user=Depends(require_roles(["Engineering", "C-Level"]))):
    log_access(
        username=user.username,
        role=user.role,
        endpoint="/engineering-data",
        action="ALLOWED"
    )
    return {
        "message": "Engineering internal data",
        "accessed_by": user.username,
        "role": user.role
    }
@app.post("/chat")
def chat(
    query: str,
    current_user=Depends(get_current_user)
):
    response = run_rag(query, current_user.role)
    return response
