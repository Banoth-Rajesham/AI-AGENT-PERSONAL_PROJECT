"""
jina_reader.py
--------------
This tool reads the text content of any web page using the Jina Reader API.
Jina converts any URL into clean, readable text — great for AI research.

Environment Variable (optional):
  - JINA_API_KEY : Your Jina API key for higher rate limits

Usage:
    from app.tools.jina_reader import read_article
    text = read_article("https://techcrunch.com")
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Jina API key (optional — works without it but with lower rate limits)
JINA_API_KEY = os.getenv("JINA_API_KEY")


def read_article(url: str) -> str:
    """
    Fetches the text content of a web page using the Jina Reader API.

    The Jina Reader API works by prepending "https://r.jina.ai/" to any URL.
    It strips away HTML and returns just the readable text.

    Args:
        url (str): The full URL of the article or web page.

    Returns:
        str: First 1500 characters of the cleaned page text.
    """

    # Jina Reader endpoint — just prefix the URL
    jina_url = f"https://r.jina.ai/{url}"

    # Add API key to headers if available
    headers = {}
    if JINA_API_KEY:
        headers["Authorization"] = f"Bearer {JINA_API_KEY}"

    # Make the request
    response = requests.get(jina_url, headers=headers)

    # Return first 1500 characters to keep the output short
    return response.text[:1500]