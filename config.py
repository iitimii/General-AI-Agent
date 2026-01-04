import os
from dotenv import load_dotenv
load_dotenv()

LLM_SETTINGS = {
    "provider": "google_genai",
    "model": "gemini-3-flash-preview",
    "api_key": os.getenv("GEMINI_API_KEY"),
    "temperature": 0
}
