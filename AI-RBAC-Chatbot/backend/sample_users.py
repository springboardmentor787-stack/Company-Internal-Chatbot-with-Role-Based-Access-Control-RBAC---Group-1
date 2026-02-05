from backend.database import SessionLocal
from backend.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

db = SessionLocal()

def create_user(username, password, role):
    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user:
        user = User(
            username=username,
            hashed_password=hash_password(password),
            role=role
        )
        db.add(user)
        print(f"User '{username}' added")
    else:
        print(f"User '{username}' already exists")

create_user("abc", "abc123", "HR")
create_user("finance1", "finance123", "Finance")
create_user("ceo", "ceo123", "C-Level")
create_user("eng", "eng345", "Engineering")
create_user("mark", "mark1234", "Marketing")

db.commit()
db.close()

print("Sample users check complete")
