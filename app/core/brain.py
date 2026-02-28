from groq import Groq
from .config import Settings


class Brain:
    def __init__(self):
        self.client = Groq(api_key=Settings.GROQ_API_KEY)
        self.model = Settings.MODEL

    def chat(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content