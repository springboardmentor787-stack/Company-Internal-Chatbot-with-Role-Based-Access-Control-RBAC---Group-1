from transformers import pipeline

# Free, local model
MODEL_NAME = "google/flan-t5-base"

print("Loading free LLM model...")
llm_pipeline = pipeline(
    "text-generation",
    model=MODEL_NAME,
    max_new_tokens=256
)

def generate_answer(prompt: str):
    result = llm_pipeline(prompt)
    return result[0]["generated_text"]
