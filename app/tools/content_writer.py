"""
content_writer.py
-----------------
Generates viral-style LinkedIn posts using the AI brain.

Usage:
    from app.tools.content_writer import create_linkedin_post
    post = create_linkedin_post("AI in Healthcare", "research text here...")
"""

from app.core.brain import Brain

# Shared Brain instance for all content writing tasks
brain = Brain()


def create_linkedin_post(topic: str, research: str) -> str:
    """
    Generates a viral LinkedIn post using AI.

    Args:
        topic (str): The subject of the post (e.g. "AI in Healthcare").
        research (str): Background information to base the post on.

    Returns:
        str: A ready-to-publish LinkedIn post.
    """

    prompt = f"""You are a viral LinkedIn content creator. Your posts always get thousands of likes.

Topic: {topic}

Research context (use only relevant parts, ignore irrelevant ones):
{research[:2000]}

Write a VIRAL LinkedIn post following ALL these rules STRICTLY:

FORMAT RULES (very important):
- Line 1: ONE powerful hook sentence. Short. Punchy. No hashtags here.
- Line 2: Empty line
- Then the body — use short punchy paragraphs (1-3 lines each), separated by empty lines
- Use → arrows, ✅ checkmarks, 🔥 emojis, or numbered points to make it scannable
- The body should have 4-6 sections or key points
- Second to last line: ONE strong call-to-action question to drive comments
- Last line: 5 relevant hashtags separated by spaces

CONTENT RULES:
- Make it feel like a real insight from someone who built something or discovered something
- Use short sentences. Like this. Not long rambling ones.
- Avoid generic fluff like "In today's fast-paced world..."
- Be specific with numbers, comparisons, or concrete examples when possible
- Sound like a senior tech professional sharing a real experience
- NEVER mention any specific news site, event, or company from the research unless it's directly relevant
- Focus 100% on the topic itself

Example structure:
I built [X] in [Y] hours. Here's what happened.

[Hook paragraph]

🔥 The Reality:
→ Point 1
→ Point 2
→ Point 3

📊 Key Insight:
[1-2 sentence insight]

[Call-to-action question]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5

Now write the post for the topic: {topic}
"""

    response = brain.chat([
        {"role": "user", "content": prompt}
    ])

    return response