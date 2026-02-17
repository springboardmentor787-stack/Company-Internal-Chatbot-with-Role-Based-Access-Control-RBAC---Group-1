from fastapi import FastAPI, Depends
from api.auth.auth_routes import router as auth_router
from api.auth.jwt_utils import get_current_user
from document_loader.secure_semantic_search import secure_semantic_search
from rag.rag_pipeline import run_rag
from rag.confidence import calculate_confidence

app = FastAPI(
    title="RBAC Semantic Search API",
    description="Company Internal Chatbot with Role-Based Access Control",
    version="1.0"
)

app.include_router(auth_router)

@app.post("/search")
def search(query: str, user=Depends(get_current_user)):
    role = user["role"]

    results = secure_semantic_search(
        query=query,
        user_role=role
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

@app.post("/rag")
def rag_query(query: str, user=Depends(get_current_user)):
    role = user["role"]

    results = secure_semantic_search(query, role)
    rag_output = run_rag(query, role, results)
    confidence = calculate_confidence(results)

    return {
        "answer": rag_output["answer"],
        "sources": rag_output["sources"],
        "confidence": confidence
    }
