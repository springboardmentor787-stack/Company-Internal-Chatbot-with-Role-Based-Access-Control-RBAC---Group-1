from milestone_3.search_service import search_with_rbac
from milestone_3.llm import generate_answer


def build_prompt(user_query: str, chunks: list):
    retrieved_chunks = ""
    for c in chunks:
        retrieved_chunks += c["text"] + "\n\n"

    prompt = f"""
You are a company assistant.
Answer strictly using the context below.
If answer is not in context, say: "I don't know".

Context:
{retrieved_chunks}

Question:
{user_query}

Answer:
"""
    return prompt


def compute_confidence(chunks: list):
    if not chunks:
        return 0.0

    # Normalize Chroma cosine distance into 0–1 confidence
    avg_dist = sum(c["distance"] for c in chunks) / len(chunks)
    confidence = 1 / (1 + avg_dist)
    return round(confidence, 2)


def rag_pipeline(query: str, user_role: str):
    chunks = search_with_rbac(query, user_role)

    # Hallucination protection (MANDATORY + relevance threshold)
    if not chunks or chunks[0]["distance"] > 2.0:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": 0.0
        }

    prompt = build_prompt(query, chunks)
    answer = generate_answer(prompt)
    confidence = compute_confidence(chunks)

    sources = list(set(c["source"] for c in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }

