from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, verify_password, create_token
from jose import jwt
from rbac import check_role
from scripts.models import User
from database import engine, SessionLocal


SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-user")
def create_user(username, password, role, db: Session = Depends(get_db)):
    user = User(
        username=username,
        password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(username, password, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username, "role": user.role})
    return {"access_token": token}

@app.get("/finance")
def finance(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    check_role(payload["role"], ["Finance", "C-Level"])
    return {"data": "Finance confidential data"}
