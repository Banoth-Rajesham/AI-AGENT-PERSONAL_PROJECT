import time
import urllib.parse


def get_images(topic: str) -> list:

    # Use only the first 3 words of the topic as keywords (cleaner search)
    words = topic.strip().split()[:3]
    keywords = ",".join(words)

    # URL-encode the keywords
    encoded = urllib.parse.quote(keywords)

    # Use timestamp as lock so each call returns a different image for same topic
    lock = int(time.time())

    # LoremFlickr: free, no API key, returns a real photo matching the keywords
    # Format: https://loremflickr.com/{width}/{height}/{keywords}?lock={seed}
    image_url = f"https://loremflickr.com/800/450/{encoded}?lock={lock}"

    return [image_url]