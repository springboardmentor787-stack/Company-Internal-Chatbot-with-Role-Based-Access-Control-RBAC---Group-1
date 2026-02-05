from backend.rag.retriever import retrieve_documents
from backend.rag.llm import generate_answer


def run_rag(query: str, role: str):
    results = retrieve_documents(query, role)

    if not results:
        return {
            "answer": "No authorized documents found.",
            "sources": [],
            "confidence": 0.0
        }

    top_results = results[:3]

    context_chunks = []
    sources = []
    scores = []

    for idx, (doc, score) in enumerate(top_results):
        context_chunks.append(doc.page_content)
        scores.append(score)

        sources.append({
            "file": doc.metadata.get("source"),
            "department": doc.metadata.get("dept"),
            "chunk_id": idx,
            "relevance_score": round(score, 2),
            "evidence": doc.page_content[:200]
        })

    context = "\n\n".join(context_chunks)

    answer = generate_answer(context, query)

    confidence = round(sum(scores) / len(scores), 2)

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "retrieved_content_preview": [
            doc.page_content[:200] for doc, _ in top_results
        ]
    }
