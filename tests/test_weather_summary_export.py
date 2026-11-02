import pytest
import json
import csv
from io import StringIO
from src.task4_weather_summary_export import summarize_weather_data, export_to_csv
from src.utils import load_json


def test_load_json(monkeypatch):
    # Mock JSON data
    mock_data = {
        "city": "Tokyo",
        "latitude": 35.6895,
        "longitude": 139.6917,
        "timezone": "Asia/Tokyo",
        "daily": [
            {
                "date": "2024-08-18",
                "max_temperature": 32.5,
                "min_temperature": 22.5,
                "precipitation": 0.0,
                "wind_speed": 15.5,
                "humidity": 65,
                "weather_description": "Clear sky"
            }
        ]
    }

    def mock_open(*args, **kwargs):
        return StringIO(json.dumps(mock_data))

    monkeypatch.setattr('builtins.open', mock_open)

    # Call the function and check the content
    data = load_json("tokyo_weather_complex.json")
    assert data["city"] == "Tokyo"
    assert len(data["daily"]) == 1


def test_summarize_weather_data():
    # Mock daily weather data
    daily_data = [
        {
            "date": "2024-08-18",
            "max_temperature": 32.5,
            "min_temperature": 22.5,
            "precipitation": 0.0,
            "wind_speed": 15.5,
            "humidity": 65,
            "weather_description": "Clear sky"
        },
        {
            "date": "2024-08-19",
            "max_temperature": 30.0,
            "min_temperature": 21.0,
            "precipitation": 5.0,
            "wind_speed": 10.0,
            "humidity": 70,
            "weather_description": "Light rain"
        }
    ]

    summary = summarize_weather_data(daily_data)

    assert summary["average_max_temp"] == (32.5 + 30.0) / 2
    assert summary["average_min_temp"] == (22.5 + 21.0) / 2
    assert summary["total_precipitation"] == 5.0
    assert summary["average_wind_speed"] == (15.5 + 10.0) / 2
    assert summary["average_humidity"] == (65 + 70) / 2
    assert summary["hot_days"] == 1
    assert summary["windy_days"] == 1
    assert summary["rainy_days"] == 1


def test_export_to_csv():
    # Mock daily weather data
    daily_data = [
        {
            "date": "2024-08-18",
            "max_temperature": 32.5,
            "min_temperature": 22.5,
            "precipitation": 0.0,
            "wind_speed": 15.5,
            "humidity": 65,
            "weather_description": "Clear sky"
        }
    ]

    # Use StringIO as a mock file
    mock_file = StringIO()

    # Call the export function with StringIO instead of a file path
    export_to_csv(daily_data, mock_file)

    # Rewind the StringIO object to the beginning
    mock_file.seek(0)

    # Read the CSV content from the StringIO object
    reader = csv.DictReader(mock_file)
    rows = list(reader)

    # Assertions to check the content of the CSV file
    assert len(rows) == 1
    assert rows[0]["Date"] == "2024-08-18"
    assert rows[0]["Max Temperature"] == "32.5"
    assert rows[0]["Min Temperature"] == "22.5"
    assert rows[0]["Precipitation"] == "0.0"
    assert rows[0]["Wind Speed"] == "15.5"
    assert rows[0]["Humidity"] == "65"
    assert rows[0]["Weather Description"] == "Clear sky"
    assert rows[0]["Is Hot Day"] == "True"
    assert rows[0]["Is Windy Day"] == "True"
    assert rows[0]["Is Rainy Day"] == "False"



if __name__ == "__main__":
    pytest.main()
