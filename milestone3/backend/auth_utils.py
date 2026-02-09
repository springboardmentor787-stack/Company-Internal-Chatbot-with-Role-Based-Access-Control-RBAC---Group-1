from passlib.context import CryptContext
from .db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "username": row[0],
        "hashed_password": row[1],
        "role": row[2]
    }

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
