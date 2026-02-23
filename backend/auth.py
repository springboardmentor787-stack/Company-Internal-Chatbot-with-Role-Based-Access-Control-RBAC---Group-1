from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.models import verify_password
from backend.database import get_db


SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def authenticate_user(username: str, password: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    print("USER FROM DB:", user)
    print("INPUT PASSWORD:", password)

    if not user:
        print("User not found")
        return None

    print("HASHED PASSWORD IN DB:", user["password"])

    if not verify_password(password, user["password"]):
        print("Password mismatch")
        return None

    print("Password matched!")
    return user

    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
