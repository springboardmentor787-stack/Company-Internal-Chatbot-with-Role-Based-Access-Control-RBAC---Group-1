def build_prompt(context_chunks, query):

    context_text = ""

    for i, chunk in enumerate(context_chunks, 1):
        context_text += f"[Source {i}]\n{chunk['text']}\n\n"

    prompt = f"""
You are a helpful internal company assistant.

Answer ONLY using the context below.
If the answer is not in the context, say:
"I do not have access to that information."

Context:
{context_text}

Question:
{query}

Answer:
"""

    return prompt, context_chunks
