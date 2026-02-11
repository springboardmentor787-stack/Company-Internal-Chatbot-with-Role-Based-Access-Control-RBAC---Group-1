"""
Handles:
- Password hashing
- JWT creation
- JWT validation
"""

import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException

SECRET_KEY = "company-secure-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"])

def hash_password(password):
    """Hash password before storing in DB."""
    return pwd_context.hash(password)

def verify_password(password, hashed):
    """Verify user entered password."""
    return pwd_context.verify(password, hashed)

def create_token(username, role):
    """Create JWT token with expiry."""
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    """Decode and validate JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
