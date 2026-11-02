import xml.etree.ElementTree as ET
from typing import Any, Dict, List

try:
    from .models import XmlWeatherDay
    from .utils import data_path, get_logger, save_models_to_csv, setup_logging
except ImportError:
    from models import XmlWeatherDay
    from utils import data_path, get_logger, save_models_to_csv, setup_logging

logger = get_logger(__file__)


def parse_weather_xml(xml_file: str) -> List[Dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
        pydantic.ValidationError: If a <day> element has missing or invalid values.
    """
    with open(xml_file, "r", encoding="utf-8") as f:
        root = ET.fromstring(f.read())

    days = [
        XmlWeatherDay.model_validate({child.tag: (child.text or "").strip() for child in day}).model_dump()
        for day in root.findall("day")
    ]
    logger.info("Parsed %d days from %s", len(days), xml_file)
    return days


def save_to_csv(data: List[Dict[str, Any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    save_models_to_csv(data, XmlWeatherDay, filename)


if __name__ == "__main__":
    setup_logging()
    try:
        save_to_csv(parse_weather_xml(data_path("weather_data.xml")))
    except Exception:
        logger.exception("Task 5 failed")
