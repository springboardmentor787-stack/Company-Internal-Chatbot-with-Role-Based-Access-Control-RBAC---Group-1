from milestone_3.search_service import search_with_rbac
from milestone_3.llm import generate_answer


def build_prompt(user_query: str, chunks: list):
    retrieved_chunks = "\n".join(
        f"- {c['text']}" for c in chunks
    )

    prompt = f"""
You are an internal company Q&A assistant.

Instructions:
- Answer using ONLY the information in the context.
- Extract factual points relevant to the question.
- Do NOT add new information.
- Present the answer clearly in 3–5 bullet points.
- If the answer is not present, reply exactly: I don't know.

Context:
{retrieved_chunks}

Question:
{user_query}

Answer:
"""
    return prompt


# ✅ Your Requested Confidence Formula (0–100%)
def compute_confidence(chunks: list):
    if not chunks:
        return 0

    avg_dist = sum(c["distance"] for c in chunks) / len(chunks)

    # Convert cosine distance to confidence (0–1)
    raw_confidence = 1 / (1 + avg_dist)

    # Convert to percentage
    confidence_percent = raw_confidence * 100

    return round(confidence_percent, 2)


def rag_pipeline(query: str, user_role: str):
    chunks = search_with_rbac(query, user_role)

    if not chunks or chunks[0]["distance"] > 2.0:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": 0
        }

    # Use top 2 best matches
    chunks = chunks[:2]

    prompt = build_prompt(query, chunks)
    answer = generate_answer(prompt)

    if not answer or not answer.strip():
        answer = "I don't know"

    confidence = compute_confidence(chunks)
    sources = list(set(c["source"] for c in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }