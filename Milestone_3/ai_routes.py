from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from milestone_3.auth import get_current_user
from milestone_3.rag import rag_pipeline
from milestone_3.rbac import RBAC_RULES
from milestone_3.logs import log_access
import time

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    start_time = time.time()

    role = current_user["role"].lower()
    username = current_user["username"]

    if role not in RBAC_RULES:
        raise HTTPException(status_code=403, detail="Role not allowed")

    result = rag_pipeline(request.query, role)

    end_time = time.time()
    response_time = round((end_time - start_time), 2)

    log_access(
        username=username,
        role=role,
        query=request.query,
        confidence=result["confidence"],
        response_time=response_time
    )

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "sources": result["sources"],
        "role": role,
        "department": role,
        "response_time": response_time
    }