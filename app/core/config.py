import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL: str = os.getenv("MODEL", "llama-3.3-70b-versatile")

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in .env file")


Settings.validate()