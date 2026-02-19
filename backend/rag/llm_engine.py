import os
import google.generativeai as genai

# 1. Initialize the API
# It will look for the key in Render's environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY is not set in environment variables!")

genai.configure(api_key=API_KEY)

# 2. Load the free, fast model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_answer(prompt):
    """
    Generates a natural language answer using Google's Gemini API.
    Works exactly the same as the local model, but uses 0MB of your server RAM!
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"