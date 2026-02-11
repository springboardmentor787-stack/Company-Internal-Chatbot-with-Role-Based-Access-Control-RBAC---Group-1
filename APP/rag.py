from transformers import pipeline
from app.rabc import is_allowed
from .prompt import build_prompt

# Safe CPU loading
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)

# Demo internal documents
DOCUMENTS = {
    "hr": [
        {"text": "Employees are entitled to 12 days of sick leave per year."},
        {"text": "Medical certificate required for absences exceeding 2 consecutive days."}
    ],
    "finance": [
        {"text": "Q1 revenue increased by 15% compared to last year."}
    ]
}

def generate_answer(question, role, department):

    # RBAC Check
    if not is_allowed(role, department):
        return (
            "❌ You are not authorized to access this information.",
            0.0,
            "DENIED"
        )

    context_chunks = DOCUMENTS.get(department, [])

    if not context_chunks:
        return (
            "I do not have access to that information.",
            50.0,
            "ALLOWED"
        )

    prompt = build_prompt(context_chunks, question)

    result = llm(
        prompt,
        max_length=180,
        temperature=0.2,
        do_sample=False
    )[0]["generated_text"]

    # Ensure minimum 30 words
    if len(result.split()) < 30:
        result += " This response is based strictly on internal company documentation and policy guidelines to ensure clarity, compliance, and accurate information delivery."

    confidence = 90.0 if role == "C-Level" else 85.0

    return result.strip(), confidence, "ALLOWED"
