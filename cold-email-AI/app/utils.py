import re

def clean_text(text: str) -> str:
    """
    Clean raw scraped text by removing HTML, URLs, special characters,
    and extra whitespace while preserving useful content.
    """
    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http[s]?://\S+", " ", text)

    # Keep alphanumerics & basic punctuation (.,!?-), remove junk
    text = re.sub(r"[^a-zA-Z0-9.,!? \-]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
