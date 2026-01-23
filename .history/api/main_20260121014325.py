from fastapi import FastAPI
from pydantic import BaseModel

from document_loader.secure_semantic_search import secure_semantic_search

app = FastAPI(
    title="RBAC Semantic Search API",
    description="Company Internal Chatbot with Role-Based Access Control",
    version="1.0"
)


# ---------- Request Schema ----------
class SearchRequest(BaseModel):
    role: str
    query: str


# ---------- Response Schema ----------
class SearchResponse(BaseModel):
    access_granted: bool
    results: list


# ---------- API Endpoint ----------
@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    results = secure_semantic_search(
        query=request.query,
        user_role=request.role
    )

    return {
        "access_granted": len(results) > 0,
        "results": [
            {
                "score": score,
                "role": doc.metadata.get("role"),
                "source": doc.metadata.get("source"),
                "preview": doc.page_content[:150]
            }
            for doc, score in results
        ]
    }
