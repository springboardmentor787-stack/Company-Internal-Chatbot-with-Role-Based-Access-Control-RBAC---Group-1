# Modified create_users.py
from database import SessionLocal, User, init_db, engine, Base
from security import hash_password

def create_users():
    # Force a clean slate
    Base.metadata.drop_all(bind=engine) 
    init_db()

    db = SessionLocal()
    users = [
        ("fin1", "fin123", "finance"),
        ("hr1", "hr123", "hr"),
        ("eng1", "eng123", "engineering"),
        ("mkt1", "mkt123", "marketing"),
        ("ceo1", "admin123", "c-level")
    ]

    for u, p, r in users:
        user = User(username=u, password_hash=hash_password(p), role=r)
        db.add(user)

    db.commit()
    db.close()
    print("✅ Users recreated with fresh hashes!")

if __name__ == "__main__":
    create_users()