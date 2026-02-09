from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.security import get_current_user
from backend.rag.retriever import retrieve_chunks
from backend.rag.prompt_builder import build_prompt
from backend.rag.answer_generator import generate_answer

from backend.logger import get_logger
logger = get_logger("chat")


router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
def chat(req: ChatRequest, user=Depends(get_current_user)):
    try:
        chunks, confidence = retrieve_chunks(req.query, user["role"])
    except PermissionError:
        return {
            "answer": "Access denied.",
            "confidence_score": 0.0,
            "sources": [],
            "role": user["role"]
        }

    prompt = build_prompt(req.query, chunks)
    answer = generate_answer(prompt)
    logger.info(f"Chat request query='{req.query}' role={user['role']}")
    logger.warning(f"Access denied for role={user['role']} query='{req.query}'")

    logger.info(
    f"Chat success role={user['role']} "
    f"confidence={confidence} "
    f"sources={len(chunks)}"
)



    return {
        "answer": answer,
        "confidence_score": confidence,
        "sources": list({c["source"] for c in chunks}),
        "role": user["role"]
    }
