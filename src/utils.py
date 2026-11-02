"""
Common utility functions for weather data processing tasks.
"""
import json
from typing import Any, Dict


def load_json(filename: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' was not found.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from '{filename}': {e.msg}", e.doc, e.pos)


def save_to_json(data: Dict[str, Any], filename: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data (dict): The data to be saved to the JSON file.
        filename (str): The name of the JSON file to save the data in.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Error writing to file '{filename}': {e}")
