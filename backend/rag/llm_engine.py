from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -------------------------------------------------------------------------
# CONFIG & MODEL LOADING
# -------------------------------------------------------------------------
MODEL_NAME = "google/flan-t5-base"  # You can swap this for 'google/flan-t5-large' if you have 16GB RAM

print(f"Loading LLM Model: {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("LLM Loaded.")

# llm_engine.py

# ... imports ...

def generate_answer(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).input_ids

    outputs = model.generate(
        input_ids,
        max_length=512,          # <--- INCREASED from 200 to 512 (More text!)
        min_length=50,           # <--- INCREASED from 20 to 50 (Forces longer answers)
        num_beams=4,
        repetition_penalty=1.3,  # <--- LOWERED slightly (1.5 was too strict, cutting answers short)
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer
