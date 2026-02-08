from transformers import pipeline


print("Loading LLM Model...")

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=256
)

print("LLM Loaded.")


def generate_answer(prompt):

    result = generator(prompt)

    return result[0]["generated_text"]
