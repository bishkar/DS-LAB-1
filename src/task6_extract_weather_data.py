import re
from typing import Any, Dict, List

try:
    from .models import TextWeatherDay
    from .utils import data_path, get_logger, save_models_to_csv, setup_logging
except ImportError:
    from models import TextWeatherDay
    from utils import data_path, get_logger, save_models_to_csv, setup_logging

logger = get_logger(__file__)

NUMBER = r"-?\d+(?:\.\d+)?"

LINE_PATTERN = re.compile(
    rf"Date:\s*(?P<date>\d{{4}}-\d{{2}}-\d{{2}}),\s*"
    rf"Max Temp:\s*(?P<max_temperature>{NUMBER})\s*C,\s*"
    rf"Min Temp:\s*(?P<min_temperature>{NUMBER})\s*C,\s*"
    rf"Humidity:\s*(?P<humidity>\d+)\s*%,\s*"
    rf"Precipitation:\s*(?P<precipitation>{NUMBER})\s*mm"
)


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    line = line.replace("﻿", "").replace(" ", " ")
    line = line.replace("Â°", "").replace("°", "")
    line = line.encode("ascii", errors="ignore").decode("ascii")
    return re.sub(r"\s+", " ", line).strip()


def extract_weather_data(text_file: str) -> List[Dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    data = []
    with open(text_file, "r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            match = LINE_PATTERN.search(clean_text(line))
            if match:
                data.append(TextWeatherDay.model_validate(match.groupdict()).model_dump())
            elif line.strip():
                logger.warning("Line %d does not match the expected format: %r", line_no, line.strip())
    logger.info("Extracted %d days from %s", len(data), text_file)
    return data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    save_models_to_csv(data, TextWeatherDay, filename)


if __name__ == "__main__":
    setup_logging()
    try:
        save_to_csv(extract_weather_data(data_path("weather_report.txt")))
    except Exception:
        logger.exception("Task 6 failed")
