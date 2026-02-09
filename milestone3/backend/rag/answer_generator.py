from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from backend.logger import get_logger
logger = get_logger("llm")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def generate_answer(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=40,
            temperature=0.0,
            do_sample=False
        )


        
    text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    

    logger.info(f"LLM prompt length={len(prompt)}")

    text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    logger.info(f"LLM answer length={len(text)}")
    return text if text else "Not found in documents."
