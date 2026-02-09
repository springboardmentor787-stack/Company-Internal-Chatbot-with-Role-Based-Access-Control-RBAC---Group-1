def build_prompt(question: str, chunks: list) -> str:
    context = "\n".join(f"- {c['text']}" for c in chunks)

    return f"""
Answer ONLY using the context.
ONE sentence.
NO summaries.
NO extra info.

Context:
{context}

Question:
{question}

Answer:
""".strip()
