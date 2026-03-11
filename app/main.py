import asyncio
import sys

# Fix for Windows: use the correct event loop policy
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.core.agent import Agent


# ──────────────────────────────────────────
# App Setup
# ──────────────────────────────────────────

app = FastAPI(title="AI Agent")

# Serve static files (CSS, screenshots, etc.) from the /static URL path
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create the AI agent (loads memory + brain on startup)
agent = Agent()


# ──────────────────────────────────────────
# Request Model
# ──────────────────────────────────────────

class ChatRequest(BaseModel):
    """
    The JSON body expected when the user sends a message.
    Example: {"message": "Hello!"}
    """
    message: str


# ──────────────────────────────────────────
# Routes
# ──────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home():
    """
    Serve the main chat UI page.
    Reads the HTML from the static index.html file.
    """
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Receive a user message and return the AI agent's response.

    Request body:
        {"message": "your question here"}

    Response:
        {"response": "the agent's reply"}
    """
    response = agent.run(request.message)
    return {"response": response}