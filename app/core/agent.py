from .brain import Brain
from .memory import Memory
from app.tools.calculator import calculator


SYSTEM_PROMPT = """
You are a helpful, friendly AI assistant.

Communication Style:
- Speak naturally and conversationally.
- Be clear and concise.
- Avoid robotic phrases like "As an AI model".
- Use light, appropriate emojis occasionally 🙂
- Keep responses human-like and warm.
- Do not over-explain unless asked.

Formatting Rules:
- Use clean paragraphs.
- Use bullet points when helpful.
- Format code properly when needed.
- Keep spacing readable.

Behavior Rules:
- If user greets, respond casually.
- If user asks technical question, answer clearly and directly.
- If message is unclear, ask for clarification politely.
- Avoid repeating the same greeting loop.
- Do not sound defensive or overly formal.
- Avoid long disclaimers.

Tone:
- Calm
- Friendly
- Confident
- Helpful

Act like a modern AI assistant similar in quality and tone to ChatGPT.
"""


class Agent:
    def __init__(self):
        self.brain = Brain()
        self.memory = Memory()
        self.memory.add("system", SYSTEM_PROMPT)

    def run(self, user_input: str) -> str:
        self.memory.add("user", user_input)

        while True:
            response = self.brain.chat(self.memory.get())

            if response.startswith("USE_TOOL"):
                try:
                    _, tool_name, tool_input = response.split(":", 2)

                    # if tool_name == "calculator":
                    #     tool_output = calculator(tool_input)
                    # else:
                    #     tool_output = "Unknown tool"

                    # Add tool result as user input so LLM finishes answer
                    # self.memory.add("assistant", response)
                    # self.memory.add("user", f"Tool result: {tool_output}")

                except Exception as e:
                    return f"Tool error: {str(e)}"

            else:
                self.memory.add("assistant", response)
                return response