from passlib.context import CryptContext
from backend.db import SessionLocal
from backend.models import User

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
db = SessionLocal()

users = [
    ("alice", "alice123", "Finance"),
    ("bob", "bob123", "HR"),
    ("carol", "carol123", "Engineering"),
    ("ceo", "ceo123", "C-Level"),
    ("mark", "mark123", "Marketing"),
    ("gen", "gen123", "General")
]

for u, p, r in users:
    if not db.query(User).filter(User.username == u).first():
        db.add(User(
            username=u,
            hashed_password=pwd.hash(p),
            role=r
        ))

db.commit()

print("Sample users inserted")
