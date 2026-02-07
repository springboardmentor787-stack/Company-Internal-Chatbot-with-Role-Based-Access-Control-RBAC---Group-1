from transformers import pipeline

class LLMClient:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=256
        )

    def generate(self, prompt: str) -> str:
        response = self.generator(prompt)
        return response[0]["generated_text"]
