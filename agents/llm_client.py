import os

# NOTE: This version relies on the 'config.py' file and the
# google-generativeai SDK setup.
from config import GEMINI_API_KEY, MODEL_NAME
import google.generativeai as genai

# Configure the model globally
LLM_MODEL = None
try:
    if not GEMINI_API_KEY:
        # In a real setup, this would fail, but for the Canvas environment,
        # we configure to allow the system to inject the key later if possible.
        # However, since this version requires the SDK setup, we keep the check.
        raise ValueError("GEMINI_API_KEY is not set in config.py.")

    # Using the google-genai library
    genai.configure(api_key=GEMINI_API_KEY)
    LLM_MODEL = genai.GenerativeModel(MODEL_NAME)
    print("--- LLM Client configured successfully ---")
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    LLM_MODEL = None


def generate_text(prompt: str) -> str:
    """Generates text using the configured Gemini model (The standard function)."""
    if LLM_MODEL is None:
        return "Error: Model not configured. Check GEMINI_API_KEY in config.py."

    try:
        response = LLM_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during text generation: {e}"

# --- Compatibility Function for Agents ---


def generate_report_content(prompt: str) -> str:
    """
    Compatibility layer for the Report Writer Agent, calling the 
    user-defined 'generate_text' function.
    """
    return generate_text(prompt)
