from typing import Any, Dict, List, TextIO, Union

try:
    from .models import DailyWeather, WeatherCsvRow, WeatherReport, WeatherSummary
    from .utils import data_path, get_logger, load_json, save_models_to_csv, setup_logging
except ImportError:
    from models import DailyWeather, WeatherCsvRow, WeatherReport, WeatherSummary
    from utils import data_path, get_logger, load_json, save_models_to_csv, setup_logging

logger = get_logger(__file__)


def summarize_weather_data(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    if not data:
        raise ValueError("No weather data to summarize.")

    days = [DailyWeather.model_validate(d).analyze() for d in data]
    n = len(days)

    def mean(attr: str) -> float:
        return sum(getattr(d, attr) for d in days) / n

    def count(attr: str) -> int:
        return sum(1 for d in days if getattr(d, attr))

    return WeatherSummary(
        average_max_temp=mean("max_temperature"),
        average_min_temp=mean("min_temperature"),
        total_precipitation=sum(d.precipitation for d in days),
        average_wind_speed=mean("wind_speed"),
        average_humidity=mean("humidity"),
        hot_days=count("is_hot_day"),
        windy_days=count("is_windy_day"),
        rainy_days=count("is_rainy_day"),
    ).model_dump()


def export_to_csv(data: List[Dict[str, Any]], file: Union[str, TextIO]) -> None:
    """
    Export the daily weather data with analysis flags to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    analyses = [DailyWeather.model_validate(d).analyze() for d in data]
    save_models_to_csv(analyses, WeatherCsvRow, file)


if __name__ == "__main__":
    setup_logging()
    try:
        report = WeatherReport.model_validate(load_json(data_path("tokyo_weather_complex.json")))
        daily = [day.model_dump() for day in report.daily]

        for key, value in summarize_weather_data(daily).items():
            logger.info("Summary %s: %s", key, value)

        export_to_csv(daily, "tokyo_weather_summary.csv")
    except Exception:
        logger.exception("Task 4 failed")
