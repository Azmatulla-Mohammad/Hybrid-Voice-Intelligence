import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load from project root .env
load_dotenv(dotenv_path="../.env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Try loading from local directory common during dev
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

print(f"Checking models for Key: {api_key[:5]}...{api_key[-5:]}")
genai.configure(api_key=api_key)

try:
    models = list(genai.list_models())
    with open("models.txt", "w", encoding="utf-8") as f:
        print("Available 'generateContent' models:")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                f.write(f"{m.name}\n")
except Exception as e:
    print(f"Error listing models: {e}")
