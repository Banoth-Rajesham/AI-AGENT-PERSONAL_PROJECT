import os
from dotenv import load_dotenv

# Load values from the .env file into environment variables
load_dotenv()


class Settings:
    """
    Central configuration class for the application.
    All settings are read from environment variables.
    """

    # Groq API key — required to call the LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    # The AI model to use (default is Llama 3.3 70B)
    MODEL: str = os.getenv("MODEL", "llama-3.3-70b-versatile")

    @classmethod
    def validate(cls):
        """
        Check that all required settings are present.
        Raises an error early if something important is missing.
        """
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing.\n"
                "Please add it to your .env file:\n"
                "  GROQ_API_KEY=your_key_here"
            )


# Run validation as soon as this module is loaded
Settings.validate()