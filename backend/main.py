from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import torch

from backend.auth import (
    authenticate_user,
    create_access_token,
    get_db,
    get_current_user
)
from backend.rbac import require_role
from backend.audit import audit_log

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from groq import Groq
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(title="Secure RAG Backend")


@app.get("/health")
def health():
    return {"status": "ok"}


# =====================================================
# Embeddings + Vector DB
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)


# =====================================================
# Load LLM (FLAN-T5)
# =====================================================

llm_model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(llm_model_name)

model = AutoModelForSeq2SeqLM.from_pretrained(
    llm_model_name,
    dtype=torch.float32
)


# =====================================================
# Authentication
# =====================================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "username": user.username,
        "role": user.role
    }


# =====================================================
# RAG CHUNKS (Retrieval Layer)
# =====================================================

@app.post("/rag-chunks")
def rag_chunks(
    payload: dict,
    request: Request,
    user=Depends(require_role(
        ["Finance", "HR", "Engineering", "Marketing", "C-Level", "General"]
    ))
):

    query = payload.get("query", "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    results = vector_db.similarity_search_with_score(query, k=5)

    visible_chunks = []
    blocked_count = 0
    allowed_scores = []

    for doc, score in results:

        allowed_roles = doc.metadata.get("allowed_roles", [])

        chunk_info = {
            "source": doc.metadata.get("source"),
            "department": doc.metadata.get("department"),
            "allowed_roles": allowed_roles,
            "content": doc.page_content
        }

        if user.role == "C-Level" or user.role in allowed_roles:
            visible_chunks.append(chunk_info)
            allowed_scores.append(score)
        else:
            blocked_count += 1

    # Confidence calculation
    if allowed_scores:
        avg_distance = sum(allowed_scores) / len(allowed_scores)
        confidence = round(1 / (1 + avg_distance), 3)
    else:
        confidence = 0.0

    # Audit status
    if not visible_chunks:
        status = "DENIED"
    elif blocked_count > 0:
        status = "PARTIAL"
    else:
        status = "ALLOWED"

    audit_log(
        user=user,
        endpoint=str(request.url.path),
        query=query,
        status=status
    )

    return {
        "query": query,
        "user_role": user.role,
        "retrieved_chunks": len(results),
        "allowed_chunks": visible_chunks,
        "blocked_chunks_count": blocked_count,
        "confidence": confidence
    }


# =====================================================
# RAG ANSWER (Full RAG Pipeline)
# =====================================================

@app.post("/rag-answer")
def rag_answer(
    payload: dict,
    request: Request,
    user=Depends(require_role(
        ["Finance", "HR", "Engineering", "Marketing", "C-Level", "General"]
    ))
):

    query = payload.get("query", "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    results = vector_db.similarity_search_with_score(query, k=5)

    allowed_chunks = []
    allowed_scores = []
    blocked = 0
    sources = []

    for doc, score in results:
        allowed_roles = doc.metadata.get("allowed_roles", [])

        if user.role == "C-Level" or user.role in allowed_roles:

            content = doc.page_content.strip()

            if content not in allowed_chunks:
                allowed_chunks.append(content)
                allowed_scores.append(score)

            src = doc.metadata.get("source")
            if src and src not in sources:
                sources.append(src)

        else:
            blocked += 1

    # Confidence
    if allowed_scores:
        avg_distance = sum(allowed_scores) / len(allowed_scores)
        confidence = round(1 / (1 + avg_distance), 3)
    else:
        confidence = 0.0

    # Status
    if not allowed_chunks:
        status = "DENIED"
    elif blocked > 0:
        status = "PARTIAL"
    else:
        status = "ALLOWED"

    if not allowed_chunks:
        audit_log(
            user=user,
            endpoint=str(request.url.path),
            query=query,
            status=status
        )

        return {
            "answer": "No authorized information found for your role.",
            "confidence": confidence,
            "sources": [],
            "blocked_chunks": blocked,
            "user_role": user.role
        }

    # Build context
    context = "\n".join(f"- {c}" for c in allowed_chunks[:3])

    prompt = f"""
You are an internal company assistant.

Use context to answer clearly.
Bullet points.
No repetition.

Context:
{context}

Question:
{query}
"""

    # GROQ CALL
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional enterprise assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()

    if not answer:
        answer = "I don't know"

    audit_log(
        user=user,
        endpoint=str(request.url.path),
        query=query,
        status=status
    )

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "blocked_chunks": blocked,
        "user_role": user.role
    }
