from api.database import engine, SessionLocal
from api.auth.user_models import Base, User
from api.auth.auth_utils import hash_password

from document_loader.chroma_store import create_chroma_db

import os
import shutil

PERSIST_DIR = "chroma_db"

# --------------------------
# 1️⃣ Create SQLite Tables
# --------------------------
def create_sqlite_db():
    Base.metadata.create_all(bind=engine)
    print("✅ SQLite tables created")


# --------------------------
# 2️⃣ Seed Default Users
# --------------------------
def seed_default_users():
    db = SessionLocal()

    default_users = [
        ("ceo", "123", "C-Level"),
        ("finance", "123", "Finance"),
        ("hruser", "123", "HR"),
        ("engg", "123", "Engineering"),
        ("marketing", "123", "Marketing"),
        ("general", "123", "General")
    ]

    for username, password, role in default_users:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            user = User(
                username=username,
                hashed_password=hash_password(password),
                role=role
            )
            db.add(user)

    db.commit()
    db.close()
    print("✅ Default users seeded")


# --------------------------
# 3️⃣ Create Vector DB
# --------------------------
def create_vector_db():
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
        print("Old Chroma DB deleted")

    create_chroma_db()
    print("✅ Chroma vector DB created")


# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":
    print("\n🔄 Initializing databases...\n")

    create_sqlite_db()
    seed_default_users()
    create_vector_db()

    print("\n🎉 System ready for deployment.")
