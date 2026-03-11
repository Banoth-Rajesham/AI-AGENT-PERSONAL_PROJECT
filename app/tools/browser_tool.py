"""
browser_tool.py
---------------
This file contains browser automation tools using Playwright.

Three tools are available:
  1. open_and_screenshot(url)  - Opens a URL and takes a screenshot
  2. google_search(query)      - Searches Google and returns top results
  3. scrape_page(url)          - Scrapes and returns text content from a URL
"""

import os
import time
from playwright.sync_api import sync_playwright


# ──────────────────────────────────────────
# TOOL 1 → Open a website and take a screenshot
# ──────────────────────────────────────────

def open_and_screenshot(url: str):
    """
    Opens a URL in a headless browser and saves a screenshot.

    Args:
        url (str): The website URL to open.

    Returns:
        tuple: (url, page_title, screenshot_filename)
    """

    # Add https:// prefix if missing
    if not url.startswith("http"):
        url = "https://" + url

    # Make sure the screenshots folder exists
    os.makedirs("app/static/screenshots", exist_ok=True)

    # Create a unique filename using current timestamp
    filename = f"screenshot_{int(time.time())}.png"
    path = f"app/static/screenshots/{filename}"

    # Launch browser, open the page, take a screenshot
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        title = page.title()
        page.screenshot(path=path)

        browser.close()

    return url, title, filename


# ──────────────────────────────────────────
# TOOL 2 → Search Google and return results
# ──────────────────────────────────────────

def google_search(query: str) -> list:
    """
    Searches Google for a query and returns the top result titles.

    Args:
        query (str): The search term.

    Returns:
        list: A list of result title strings (up to 5).
    """

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to Google
        page.goto("https://www.google.com")

        # Type the search query into the search box
        page.fill("textarea[name='q']", query)

        # Press Enter to search  ← fixed typo: was "page.keybord.press"
        page.keyboard.press("Enter")

        # Wait until search results appear
        page.wait_for_selector("h3")

        # Grab the top 5 result headings
        elements = page.query_selector_all("h3")
        for el in elements[:5]:
            results.append(el.inner_text())

        browser.close()

    return results


# ──────────────────────────────────────────
# TOOL 3 → Scrape text content from a URL
# ──────────────────────────────────────────

def scrape_page(url: str) -> str:
    """
    Opens a URL and extracts all visible text from the page body.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: First 1500 characters of the page text.
    """

    # Add https:// prefix if missing  ← fixed typo: was "url.startwith"
    if not url.startswith("http"):
        url = "https://" + url

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        # Get all visible text from the page body
        text = page.inner_text("body")

        browser.close()

    # Return first 1500 characters to keep the output manageable
    return text[:1500]
