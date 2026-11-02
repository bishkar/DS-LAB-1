import pytest
import requests
import json
from src.task2_fetch_tokyo_weather import fetch_weather_data
from src.utils import save_to_json


def test_fetch_weather_data(monkeypatch):
    # Mock response for the Open-Meteo API
    class MockResponse:
        @staticmethod
        def raise_for_status():
            pass

        @staticmethod
        def json():
            return {
                "daily": {
                    "time": ["2024-08-18"],
                    "temperature_2m_max": [32.5]
                }
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    # Use monkeypatch to replace requests.get with mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # Call the function and check the returned data
    weather_data = fetch_weather_data()
    assert weather_data == {"date": "2024-08-18", "max_temperature": 32.5}


def test_save_to_json(tmpdir):
    # Mock data to save
    data = {"date": "2024-08-18", "max_temperature": 32.5}

    # Use a temporary directory to save the JSON file
    temp_file = tmpdir.join("test_tokyo_weather.json")

    # Call the function to save data
    save_to_json(data, temp_file)

    # Read the file and check the contents
    with open(temp_file, 'r') as f:
        saved_data = json.load(f)

    assert saved_data == data


if __name__ == "__main__":
    pytest.main()
