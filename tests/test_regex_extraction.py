import pytest
from io import StringIO
from src.task6_extract_weather_data import extract_weather_data, save_to_csv  # Import your functions


def create_sample_text():
    """
    Create a sample text data for testing.
    """
    return """Date: 2024-08-18, Max Temp: 32.9°C, Min Temp: 22.5°C, Humidity: 65%, Precipitation: 0.0mm
Date: 2024-08-19, Max Temp: 30.5°C, Min Temp: 21.8°C, Humidity: 70%, Precipitation: 1.2mm
"""


def test_extract_weather_data(monkeypatch):
    # Create a sample text data
    text_data = create_sample_text()

    # Use StringIO to mock a file object
    text_file = StringIO(text_data)

    # Mock the file opening and reading process
    def mock_open(*args, **kwargs):
        return text_file

    monkeypatch.setattr('builtins.open', mock_open)

    # Extract the data using regex
    extracted_data = extract_weather_data("mock_file.txt")

    assert len(extracted_data) == 2
    assert extracted_data[0]['date'] == '2024-08-18'
    assert extracted_data[0]['max_temperature'] == 32.9
    assert extracted_data[0]['min_temperature'] == 22.5
    assert extracted_data[0]['humidity'] == 65
    assert extracted_data[0]['precipitation'] == 0.0

    assert extracted_data[1]['date'] == '2024-08-19'
    assert extracted_data[1]['max_temperature'] == 30.5
    assert extracted_data[1]['min_temperature'] == 21.8
    assert extracted_data[1]['humidity'] == 70
    assert extracted_data[1]['precipitation'] == 1.2


def test_save_to_csv(tmpdir):
    # Sample extracted data
    data = [
        {"date": "2024-08-18", "max_temperature": 32.9, "min_temperature": 22.5, "humidity": 65, "precipitation": 0.0},
        {"date": "2024-08-19", "max_temperature": 30.5, "min_temperature": 21.8, "humidity": 70, "precipitation": 1.2}
    ]

    # Use a temporary directory to save the CSV
    temp_csv_file = tmpdir.join("test_extracted_weather_data.csv")
    save_to_csv(data, filename=str(temp_csv_file))

    # Check the contents of the CSV
    with open(temp_csv_file, 'r') as file:
        lines = file.readlines()

    assert lines[0].strip() == "Date,Max Temperature,Min Temperature,Humidity,Precipitation"
    assert lines[1].strip() == "2024-08-18,32.9,22.5,65,0.0"
    assert lines[2].strip() == "2024-08-19,30.5,21.8,70,1.2"
