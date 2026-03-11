from .brain import Brain
from .memory import Memory
from app.tools.browser_tool import open_and_screenshot, google_search, scrape_page
from app.tools.jina_reader import read_article
from app.tools.content_writer import create_linkedin_post
from app.tools.image_search import get_images


# The system prompt sets the personality and behavior of the AI assistant.
# This is always the first message sent to the LLM.
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
- If user asks a technical question, answer clearly and directly.
- If the message is unclear, ask for clarification politely.
- Avoid repeating the same greeting loop.
- Do not sound defensive or overly formal.
- Avoid long disclaimers.

Tone: Calm, Friendly, Confident, Helpful.
"""


class Agent:
    """
    The main agent that handles user messages and decides what to do with them.
    """

    def __init__(self):
        # Brain → handles AI/LLM calls
        self.brain = Brain()

        # Memory → stores conversation history
        self.memory = Memory()

        # Add the system prompt as the very first message in memory
        self.memory.add("system", SYSTEM_PROMPT)

    def run(self, user_input: str) -> str:
        """
        Process a user message and return a response.

        First checks if the message is a special command.
        If not, falls back to normal LLM chat.

        Args:
            user_input (str): The raw message from the user.

        Returns:
            str or dict: The agent's response (string for chat, dict for LinkedIn post).
        """

        # Use lowercase version only for command matching (not for display)
        text = user_input.lower().strip()

        # ──────────────────────────────────────────
        # COMMAND 1 → Open a website + take screenshot
        # Example: "auto open google.com"
        # ──────────────────────────────────────────
        if text.startswith("auto open "):
            url = user_input.replace("auto open ", "").strip()

            url, title, screenshot = open_and_screenshot(url)

            return (
                f"✅ Opened: {url}\n\n"
                f"📄 Title: {title}\n\n"
                f"📸 Screenshot:\n"
                f"http://127.0.0.1:8000/static/screenshots/{screenshot}"
            )

        # ──────────────────────────────────────────
        # COMMAND 2 → Search Google
        # Example: "auto search google for Python tutorials"
        # ──────────────────────────────────────────
        if text.startswith("auto search google for "):
            query = user_input.replace("auto search google for ", "").strip()

            results = google_search(query)

            # Format results as a numbered list
            numbered = "\n".join([f"{i+1}. {r}" for i, r in enumerate(results)])

            return f"🔎 Google Results for: {query}\n\n{numbered}"

        # ──────────────────────────────────────────
        # COMMAND 3 → Scrape text from a URL
        # Example: "auto scrape https://example.com"
        # ──────────────────────────────────────────
        if text.startswith("auto scrape "):
            url = user_input.replace("auto scrape ", "").strip()

            content = scrape_page(url)

            return f"🌐 Scraped Content from: {url}\n\n{content}"

        # ──────────────────────────────────────────
        # COMMAND 4 → Create a LinkedIn post
        # Example: "create linkedin post about AI in healthcare"
        # ──────────────────────────────────────────
        if "linkedin" in text.replace(" ", "") and "post" in text:
            topic = user_input

            # Gather research from tech news sites
            research_sources = [
                "https://techcrunch.com",
                "https://venturebeat.com",
                "https://www.theverge.com"
            ]

            research = ""
            for url in research_sources:
                article = read_article(url)
                research += article + "\n\n"

            # Keep research under 4000 chars to fit in the LLM prompt
            research = research[:4000]

            # Generate the LinkedIn post using AI
            post = create_linkedin_post(topic, research)

            # Get suggested images from Unsplash
            images = get_images(topic)

            return {
                "type": "post",
                "platform": "linkedin",
                "content": post,
                "images": images
            }

        # ──────────────────────────────────────────
        # DEFAULT → Normal AI chat
        # ──────────────────────────────────────────
        # Add the user's message to memory
        self.memory.add("user", user_input)

        # Ask the LLM to generate a reply using the full conversation history
        response = self.brain.chat(self.memory.get())

        # Save the AI's reply to memory for future context
        self.memory.add("assistant", response)

        return response