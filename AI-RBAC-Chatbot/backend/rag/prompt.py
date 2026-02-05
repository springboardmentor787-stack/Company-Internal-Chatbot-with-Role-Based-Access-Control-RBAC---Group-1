def build_prompt(query: str, documents: list) -> str:
    """
    Builds a clean prompt with retrieved context.
    """

    context = ""
    for doc in documents:
        context += f"- {doc.page_content}\n"

    prompt = f"""
You are a company internal assistant.
Answer the question ONLY using the context below.
If the answer is not present, say "I don't have enough information".

Context:
{context}

Question:
{query}

Answer:
"""
    return prompt
