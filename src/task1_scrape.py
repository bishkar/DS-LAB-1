import re

import requests
from bs4 import BeautifulSoup

try:
    from .models import WikipediaExtract
    from .utils import get_logger, save_to_json, setup_logging
except ImportError:
    from models import WikipediaExtract
    from utils import get_logger, save_to_json, setup_logging

logger = get_logger(__file__)

HEADERS = {"User-Agent": "DS-Lab-1/1.0 (educational web scraping exercise)"}


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page to fetch.

    Returns:
        str: The HTML content of the page as a string.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
    """
    logger.info("Fetching %s", url)
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    logger.debug("Received %d characters of HTML", len(response.text))
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The title of the page.
    """
    heading = soup.find("h1", id="firstHeading")
    if heading is None:
        raise ValueError("Page title (<h1 id='firstHeading'>) not found.")
    return heading.get_text(strip=True)


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed HTML.

    Returns:
        str: The first sentence of the first paragraph.
    """
    for paragraph in soup.find_all("p"):
        text = re.sub(r"\[[^\]]*\]", "", paragraph.get_text())
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue  # Wikipedia often has empty placeholder paragraphs
        match = re.match(r"(.+?[.!?])(?=\s|$)", text)
        return match.group(1) if match else text
    raise ValueError("No non-empty paragraph found on the page.")


if __name__ == "__main__":
    setup_logging()
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        soup = BeautifulSoup(fetch_wikipedia_page(url), 'html.parser')

        extracted_data = WikipediaExtract(
            title=extract_title(soup),
            first_sentence=extract_first_sentence(soup),
        )
        logger.info("Extracted data: %s", extracted_data.model_dump())

        save_to_json(extracted_data, 'extracted_wikipedia_data.json')
    except Exception:
        logger.exception("Task 1 failed")
