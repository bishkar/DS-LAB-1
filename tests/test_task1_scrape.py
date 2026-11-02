import pytest
import requests
from bs4 import BeautifulSoup
import json
from src.task1_scrape import fetch_wikipedia_page, extract_title, extract_first_sentence
from src.utils import save_to_json


def test_fetch_wikipedia_page(monkeypatch):
    # Mock response for the Wikipedia page
    class MockResponse:
        @staticmethod
        def raise_for_status():
            pass

        @property
        def text(self):
            return '<html><head><title>Web scraping</title></head><body><h1 id="firstHeading">Web scraping</h1><p>Web scraping is the process.</p></body></html>'

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    # Call the function and check the content
    page_content = fetch_wikipedia_page("https://en.wikipedia.org/wiki/Web_scraping")
    assert "Web scraping" in page_content


def test_extract_title():
    # Mock soup object
    html = '<html><body><h1 id="firstHeading">Web scraping</h1></body></html>'
    soup = BeautifulSoup(html, 'html.parser')

    # Call the function and check the title
    title = extract_title(soup)
    assert title == "Web scraping"


def test_extract_first_sentence():
    # Mock soup object
    html = '<html><body><p>Web scraping is the process of using bots to extract content. It is widely used.</p></body></html>'
    soup = BeautifulSoup(html, 'html.parser')

    # Call the function and check the first sentence
    first_sentence = extract_first_sentence(soup)
    assert first_sentence == "Web scraping is the process of using bots to extract content."


def test_save_to_json(tmpdir):
    # Mock data to save
    data = {
        "title": "Web scraping",
        "first_sentence": "Web scraping is the process of using bots to extract content."
    }

    # Use a temporary directory to save the JSON file
    temp_file = tmpdir.join("test.json")

    # Call the function to save data
    save_to_json(data, temp_file)

    # Read the file and check the contents
    with open(temp_file, 'r') as f:
        saved_data = json.load(f)

    assert saved_data == data


if __name__ == "__main__":
    pytest.main()
