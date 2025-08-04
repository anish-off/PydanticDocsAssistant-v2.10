import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    PYDANTIC_DOCS_URL: str = os.getenv("PYDANTIC_DOCS_URL", "https://docs.pydantic.dev/2.10/")

settings = Settings()