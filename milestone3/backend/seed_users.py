import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from passlib.context import CryptContext
from backend.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_users():
    users = [
        ("employee1", "password123", "Employees"),
        ("finance1", "password123", "Finance"),
        ("hr1", "password123", "HR"),
        ("engineer1", "password123", "Engineering"),
        ("ceo1", "password123", "C-Level"),
    ]

    conn = get_db()
    cursor = conn.cursor()

    for username, password, role in users:
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, pwd_context.hash(password), role)
            )
        except:
            pass

    conn.commit()
    conn.close()
    print("Users seeded")

if __name__ == "__main__":
    seed_users()
