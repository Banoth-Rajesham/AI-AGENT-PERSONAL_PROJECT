import groq
from groq import Groq
from .config import Settings


class Brain:
    """
    Wraps the Groq API client to send and receive chat messages.
    """

    def __init__(self):
        # Create the Groq API client using the API key from settings
        self.client = Groq(api_key=Settings.GROQ_API_KEY)

        # The LLM model to use (e.g. "llama-3.3-70b-versatile")
        self.model = Settings.MODEL

    def chat(self, messages: list) -> str:
        """
        Send a list of messages to the LLM and get a reply.

        Args:
            messages (list): Conversation history in this format:
                [
                    {"role": "system",    "content": "You are helpful."},
                    {"role": "user",      "content": "Hello!"},
                    {"role": "assistant", "content": "Hi there!"},
                ]

        Returns:
            str: The AI's response text.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0   # 0 = deterministic / consistent answers
            )
            # Extract and return just the text content from the response
            return response.choices[0].message.content
        
        except groq.APIConnectionError:
            return "Oops! I couldn't connect to my AI server. Please check your internet connection or try again in a moment."
        except groq.APIError as e:
            return f"Oops! I got an error from the AI server: {e}"
        except Exception as e:
            return f"Oops! An unexpected error occurred: {e}"