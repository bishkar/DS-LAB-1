"""
Test suite for common utility functions in src/utils.py
"""
import pytest
import json
from src.utils import load_json, save_to_json


def test_save_to_json(tmpdir):
    """Test saving data to JSON file with UTF-8 encoding."""
    # Mock data to save
    data = {
        "title": "Web scraping",
        "first_sentence": "Web scraping is the process of using bots to extract content.",
        "unicode_test": "Temperature: 32°C"
    }

    # Use a temporary directory to save the JSON file
    temp_file = tmpdir.join("test.json")

    # Call the function to save data
    save_to_json(data, str(temp_file))

    # Read the file and check the contents
    with open(temp_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    assert saved_data == data
    assert saved_data["unicode_test"] == "Temperature: 32°C"


def test_load_json(tmpdir):
    """Test loading data from JSON file."""
    # Create a test JSON file
    test_data = {
        "city": "Tokyo",
        "temperature": 25.5,
        "weather": "Sunny"
    }
    
    temp_file = tmpdir.join("test_load.json")
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    # Load the file using the utility function
    loaded_data = load_json(str(temp_file))

    assert loaded_data == test_data


def test_load_json_file_not_found():
    """Test that load_json raises FileNotFoundError for non-existent files."""
    with pytest.raises(FileNotFoundError) as excinfo:
        load_json("nonexistent_file.json")
    
    assert "nonexistent_file.json" in str(excinfo.value)


def test_load_json_invalid_json(tmpdir):
    """Test that load_json raises JSONDecodeError for invalid JSON."""
    # Create a file with invalid JSON
    temp_file = tmpdir.join("invalid.json")
    with open(temp_file, 'w') as f:
        f.write("{invalid json content")

    with pytest.raises(json.JSONDecodeError):
        load_json(str(temp_file))


def test_save_to_json_io_error(tmpdir):
    """Test that save_to_json handles IO errors appropriately."""
    # Try to write to a directory path instead of a file
    invalid_path = tmpdir.mkdir("subdir")
    
    with pytest.raises(IOError):
        save_to_json({"test": "data"}, str(invalid_path))


if __name__ == "__main__":
    pytest.main()
