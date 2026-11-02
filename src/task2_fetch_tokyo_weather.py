from typing import Any, Dict

import requests

try:
    from .models import OpenMeteoResponse, TemperatureForecast
    from .utils import get_logger, save_to_json, setup_logging
except ImportError:
    from models import OpenMeteoResponse, TemperatureForecast
    from utils import get_logger, save_to_json, setup_logging

logger = get_logger(__file__)


def fetch_weather_data() -> Dict[str, Any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature
        (for the next day when the API returns several days).

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        pydantic.ValidationError: If the expected data is not in the API response.
    """
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")

    logger.info("Requesting Open-Meteo forecast for Tokyo")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    daily = OpenMeteoResponse.model_validate(response.json()).daily
    if not daily.time:
        raise ValueError("The API response contains no forecast days.")
    logger.debug("API returned %d forecast days", len(daily.time))

    index = 1 if len(daily.time) > 1 else 0  # next day if available
    forecast = TemperatureForecast(
        date=daily.time[index],
        max_temperature=daily.temperature_2m_max[index],
    )
    logger.info("Max temperature on %s: %s°C", forecast.date, forecast.max_temperature)
    return forecast.model_dump()


if __name__ == "__main__":
    setup_logging()
    try:
        save_to_json(fetch_weather_data(), "tokyo_weather.json")
    except Exception:
        logger.exception("Task 2 failed")
