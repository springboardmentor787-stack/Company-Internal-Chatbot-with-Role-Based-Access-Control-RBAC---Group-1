from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from sqlalchemy.orm import Session

# Project imports
from database import SessionLocal, User
from security import verify_password
from jwt_utils import SECRET_KEY, ALGORITHM
from retriever import retrieve_chunks
from llm_engine import generate_answer
from rbac_rules import get_allowed_departments

# -------------------------------
# CONFIG
# -------------------------------

ACCESS_TOKEN_EXPIRE_MINUTES = 60
DATA_PATH = "data"  # <--- Ensure this points to your actual data folder

app = FastAPI(title="Company RBAC Chatbot")

# Swagger UI Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------
# DATABASE DEPENDENCY
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# MODELS
# -------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class ChatInput(BaseModel):
    department: str
    question: str

# -------------------------------
# SECURITY UTILS
# -------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        return {"username": username, "role": role.lower()}
    except JWTError:
        raise credentials_exception

# -------------------------------
# HELPER: QUERY EXPANSION
# -------------------------------
def expand_query(original_query):
    """
    Uses the LLM to rewrite the user's question into a better search query.
    """
    prompt = f"""
    Rewrite the following user question to be more professional and keyword-rich for a corporate document search.
    
    User Question: {original_query}
    
    Rewritten Question:
    """
    
    # We reuse your existing LLM engine to do the rewriting!
    try:
        expanded_query = generate_answer(prompt)
        print(f"🔄 Query Expansion: '{original_query}' -> '{expanded_query.strip()}'")
        return expanded_query.strip()
    except Exception as e:
        print(f"⚠️ Expansion failed: {e}. Using original query.")
        return original_query

# -------------------------------
# 1. LOGIN API
# -------------------------------
@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# -------------------------------
# 2. CHAT API
# -------------------------------
@app.post("/chat")
def chat(
    data: ChatInput,
    current_user: dict = Depends(get_current_user_role)
):
    user_role = current_user["role"]
    target_department = data.department.lower().strip()
    question = data.question.strip()

    # --- RBAC CHECK ---
    allowed_depts = get_allowed_departments(user_role)
    if target_department not in allowed_depts:
        raise HTTPException(
            status_code=403, 
            detail=f"Access Denied: You ({user_role}) cannot access '{target_department}' data."
        )

    # --- SEARCH SCOPE EXPANSION ---
    search_scope = [target_department]
    if "general" in allowed_depts and "general" not in search_scope:
        search_scope.append("general")

    # ---------------------------------------------------------
    # 1. EXPAND THE QUERY
    # ---------------------------------------------------------
    search_query = expand_query(question)

    # ---------------------------------------------------------
    # 2. RETRIEVE (Using the Expanded Query)
    # ---------------------------------------------------------
    results = retrieve_chunks(
        query=search_query,  
        role=user_role,
        allowed_departments=search_scope,
        top_k=2
    )

    # ---------------------------------------------------------
    # 3. FILTER LOW CONFIDENCE (Threshold: 35%)
    # ---------------------------------------------------------
    # Adjusted to 35 to allow short HR answers while filtering noise
    valid_results = [r for r in results if r['confidence'] >= 35]

    if not valid_results:
        return {
            "answer": "I could not find sufficiently relevant information in your authorized documents to answer this. (Low Confidence)",
            "sources": []
        }

    # ---------------------------------------------------------
    # 4. GENERATE DETAILED ANSWER
    # ---------------------------------------------------------
    context_text = "\n\n".join([r["chunk"] for r in valid_results])
    
    prompt = f"""
    Use the following context to provide a detailed and comprehensive answer to the question.
    If the context contains a list, include all items. 
    
    Context:
    {context_text}
    
    Question: {question}
    Detailed Answer:
    """
    
    # Safety truncation
    if len(prompt) > 2000: prompt = prompt[:2000]

    answer = generate_answer(prompt)

    return {"answer": answer, "sources": valid_results}

# -------------------------------
# 3. FILE LISTING API
# -------------------------------
@app.get("/files")
def get_accessible_files(current_user: dict = Depends(get_current_user_role)):
    """
    Returns a list of files visible to the logged-in user.
    """
    user_role = current_user["role"]
    allowed_depts = get_allowed_departments(user_role)
    
    accessible_files = {}
    
    for dept in allowed_depts:
        dept_path = os.path.join(DATA_PATH, dept)
        
        if os.path.exists(dept_path):
            try:
                # Get only files, ignore subfolders
                files = [f for f in os.listdir(dept_path) if os.path.isfile(os.path.join(dept_path, f))]
                accessible_files[dept] = files
            except Exception as e:
                accessible_files[dept] = [f"Error reading folder: {str(e)}"]
        else:
            accessible_files[dept] = [] 
            
    return {"files": accessible_files}