def build_prompt(context_chunks, query):

    context_text = ""

    for i, chunk in enumerate(context_chunks, 1):
        context_text += f"[Source {i}]\n{chunk['text']}\n\n"

    prompt = f"""
You are a professional internal company assistant.

STRICT RULES:
- Answer ONLY using the provided context.
- If not found, say:
  "I do not have access to that information."
- Keep answer concise.

CONTEXT:
{context_text}

QUESTION:
{query}

FINAL ANSWER:
"""

    return prompt.strip()
