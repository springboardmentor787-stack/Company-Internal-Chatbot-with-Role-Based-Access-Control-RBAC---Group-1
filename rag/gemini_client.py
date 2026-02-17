import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

class LLMClient:
    def __init__(self):
        self.model = "gemini-2.5-flash"
        self.config = types.GenerateContentConfig(
    temperature=0.1,          # more factual
    max_output_tokens=900,    # allow full structured answers
)

    def generate(self, prompt: str) -> str:
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.config
            )

            if not response.candidates:
                return "No response generated."

            candidate = response.candidates[0]

            
            full_text = ""
            for part in candidate.content.parts:
                if hasattr(part, "text"):
                    full_text += part.text

            return full_text.strip()

        except Exception as e:
            print("Gemini Error:", str(e))
            return "An error occurred while generating the response."


