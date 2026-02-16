from transformers import pipeline

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=256
)

def generate_answer(context: str, question: str):
    if not context.strip():
        return "No relevant content found in authorized documents."

    prompt = f"""
You are a company internal assistant.

RULES:
- Use ONLY the context below
- Do NOT make up answers
- If the answer is not in the context, say: "Not found in authorized documents"

CONTEXT:
{context}

QUESTION:
{question}

FINAL ANSWER (one paragraph):
"""

    result = qa_pipeline(prompt)

    text = result[0]["generated_text"]

    if "FINAL ANSWER" in text:
        return text.split("FINAL ANSWER")[-1].strip()

    return text.strip()