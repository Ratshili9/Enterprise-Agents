import os
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

# Configure the model globally
try:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
        
    genai.configure(api_key=GEMINI_API_KEY)
    LLM_MODEL = genai.GenerativeModel(MODEL_NAME)
    print("--- LLM Client configured successfully ---")
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    LLM_MODEL = None

def generate_text(prompt: str) -> str:
    """Generates text using the configured Gemini model."""
    if LLM_MODEL is None:
        return "Error: Model not configured. Check GEMINI_API_KEY."
        
    try:
        response = LLM_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during text generation: {e}"