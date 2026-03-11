"""
research_tool.py
----------------
This tool gathers research from multiple tech news websites
using the Jina Reader API.

Usage:
    from app.tools.research_tool import research_topic
    text = research_topic("artificial intelligence")
"""

from app.tools.jina_reader import read_article


def research_topic(topic: str) -> str:
    """
    Collects articles from a few tech news websites related to a topic.

    Note: The topic isn't used to filter yet — it reads the homepage
    of each source and returns the combined text as research material.

    Args:
        topic (str): The subject you want to research.

    Returns:
        str: Combined text (up to 4000 characters) from all sources.
    """

    # List of tech news sources to read from
    # ← Fixed typos: "vebturebeat" → "venturebeat", "https//" → "https://"
    sources = [
        "https://techcrunch.com",
        "https://venturebeat.com",
        "https://www.theverge.com"
    ]

    combined_research = ""

    for url in sources:
        # Read the article text from each source
        article_text = read_article(url)
        combined_research += article_text + "\n\n"

    # Limit total output to 4000 characters to keep LLM prompts manageable
    return combined_research[:4000]