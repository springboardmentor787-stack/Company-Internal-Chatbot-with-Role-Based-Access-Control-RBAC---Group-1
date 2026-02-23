from preprocessing.rbac_config import ROLE_HIERARCHY
from preprocessing.rbac_search import rbac_semantic_search
from backend.llm import generate_answer


def build_prompt(user_query: str, chunks: list):
    retrieved_chunks = "\n".join(
        f"- {doc.page_content}" for doc, _ in chunks
    )

    prompt = f"""
You are a professional internal company assistant.

Answer the question using ONLY the information provided in the context.

Instructions:
- Write a complete 2–3 sentence answer.
- Mention important details like growth, drivers, or trends if available.
- Do NOT respond with just a number.
- Do NOT hallucinate.
- If answer not found, reply exactly: I don't know.

Context:
{retrieved_chunks}

Question:
{user_query}

Answer:
"""
    return prompt.strip()

def compute_confidence(chunks: list):
    if not chunks:
        return 0.0

    # average distance
    distances = [score for _, score in chunks]
    avg_distance = sum(distances) / len(distances)

    # convert distance → confidence
    confidence = 1 / (1 + avg_distance)

    return round(confidence, 2)


def rag_pipeline(query: str, user_role: str):

    allowed_departments = ROLE_HIERARCHY.get(user_role)

    if not allowed_departments:
        return {
            "answer": "Invalid role",
            "sources": [],
            "confidence": 0.0
        }

    all_results = []

    # 🔎 Search across all allowed departments
    for dept in allowed_departments:
        status, results = rbac_semantic_search(
            role=user_role,
            department=dept,
            query=query
        )

        if status == "Access granted" and results:
            all_results.extend(results)

    # ❌ No results
    if not all_results:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": 0.0
        }

    # 🎯 Sort by best similarity (lower distance = better)
    all_results = sorted(all_results, key=lambda x: x[1])

    # Take top 3
    top_chunks = all_results[:3]

    # 🧠 Build prompt
    prompt = build_prompt(query, top_chunks)

    # 🤖 Generate answer
    answer = generate_answer(prompt)

    if not answer or not answer.strip():
        answer = "I don't know"

    # 📊 Confidence
    confidence = compute_confidence(top_chunks)

    # 📚 Sources
    sources = list(set(
        doc.metadata.get("source_file", "Unknown")
        for doc, _ in top_chunks
    ))

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }
