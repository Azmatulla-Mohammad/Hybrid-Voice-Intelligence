import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env"))

class Settings:
    PROJECT_NAME: str = "EDITH AI"
    VERSION: str = "2.0.0"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()
