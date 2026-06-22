from transformers import pipeline

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base"
)

def generate_answer(query: str, chunks: list[str]) -> str:
    if not chunks:
        return "I don't have access to that information."

    context = " ".join(chunks[:3])

    prompt = f"""
    Answer the question using the context below.
    If the answer is not present, say you don't have access.

    Context:
    {context}

    Question:
    {query}
    """

    result = qa_pipeline(
        prompt,
        max_length=256,
        do_sample=False
    )

    return result[0]["generated_text"]
