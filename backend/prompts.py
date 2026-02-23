# backend/prompts.py

def build_prompt(query: str, chunks: list):

    context = "\n\n".join(
        f"- {doc.page_content}"
        for doc, _ in chunks[:3]   # limit context (important)
    )

    prompt = f"""
You are a secure internal company assistant.

STRICT RULES:
- Use ONLY the information in the context.
- Do NOT add outside knowledge.
- If answer not present, reply exactly: I don't know.
- Respond in clear bullet points.
- Keep answer concise.

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt
