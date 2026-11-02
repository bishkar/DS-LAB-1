import pytest
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree.ElementTree import ElementTree
import os
from io import StringIO
from src.task5_parse_weather_xml import parse_weather_xml, save_to_csv  # Import your functions


def create_sample_xml():
    """
    Create a sample XML file for testing.
    """
    weather = Element('weather')

    day1 = SubElement(weather, 'day')
    SubElement(day1, 'date').text = '2024-08-18'
    SubElement(day1, 'temperature').text = '32.9'
    SubElement(day1, 'humidity').text = '65'
    SubElement(day1, 'precipitation').text = '0.0'

    day2 = SubElement(weather, 'day')
    SubElement(day2, 'date').text = '2024-08-19'
    SubElement(day2, 'temperature').text = '30.5'
    SubElement(day2, 'humidity').text = '70'
    SubElement(day2, 'precipitation').text = '1.2'

    xml_data = tostring(weather, encoding='unicode')
    return xml_data


def test_parse_weather_xml(monkeypatch):
    # Create a sample XML structure
    xml_data = create_sample_xml()

    # Use StringIO to mock a file object
    xml_file = StringIO(xml_data)

    # Mock the file opening and reading process
    def mock_open(*args, **kwargs):
        return xml_file

    monkeypatch.setattr('builtins.open', mock_open)

    # Parse the XML and check the result
    parsed_data = parse_weather_xml("mock_file.xml")

    assert len(parsed_data) == 2
    assert parsed_data[0]['date'] == '2024-08-18'
    assert parsed_data[0]['temperature'] == 32.9
    assert parsed_data[0]['humidity'] == 65
    assert parsed_data[0]['precipitation'] == 0.0

    assert parsed_data[1]['date'] == '2024-08-19'
    assert parsed_data[1]['temperature'] == 30.5
    assert parsed_data[1]['humidity'] == 70
    assert parsed_data[1]['precipitation'] == 1.2


def test_save_to_csv(tmpdir):
    # Sample parsed data
    data = [
        {"date": "2024-08-18", "temperature": 32.9, "humidity": 65, "precipitation": 0.0},
        {"date": "2024-08-19", "temperature": 30.5, "humidity": 70, "precipitation": 1.2}
    ]

    # Use a temporary directory to save the CSV
    temp_csv_file = tmpdir.join("test_weather_data.csv")
    save_to_csv(data, filename=str(temp_csv_file))

    # Check the contents of the CSV
    with open(temp_csv_file, 'r') as file:
        lines = file.readlines()

    assert lines[0].strip() == "Date,Temperature,Humidity,Precipitation"
    assert lines[1].strip() == "2024-08-18,32.9,65,0.0"
    assert lines[2].strip() == "2024-08-19,30.5,70,1.2"
