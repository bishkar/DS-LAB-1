from typing import Any, Dict, List

try:
    from .models import DailyAnalysis, DailyWeather, Thresholds, WeatherReport
    from .utils import data_path, get_logger, load_json, setup_logging
except ImportError:
    from models import DailyAnalysis, DailyWeather, Thresholds, WeatherReport
    from utils import data_path, get_logger, load_json, setup_logging

logger = get_logger(__file__)


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30,
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    thresholds = Thresholds(hot_temperature=temp_threshold, windy_speed=wind_threshold,
                            uncomfortable_humidity=humidity_threshold)
    return DailyWeather.model_validate(day).analyze(thresholds).model_dump()


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    a = DailyAnalysis.model_validate(analysis)
    lines = [
        f"Date: {a.date}",
        f"Weather: {a.weather_description}",
        f"Temperature: Max {a.max_temperature:.1f}°C, Min {a.min_temperature:.1f}°C "
        f"(Swing: {a.temperature_swing:.1f}°C)",
    ]
    flags = [
        (a.is_hot_day, "It was a hot day."),
        (a.is_significant_swing, "There was a significant temperature swing."),
        (a.is_windy_day, "It was a windy day."),
        (a.is_uncomfortable_day, "The humidity made the day uncomfortable."),
    ]
    lines += [message for flag, message in flags if flag]
    lines.append(
        f"It was a rainy day ({a.rain_severity} rain, {a.precipitation:.1f} mm)."
        if a.is_rainy_day else "There was no precipitation."
    )
    return "\n".join(lines) + "\n"


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    if not analyses:
        return "Weather Summary:\nNo data available."

    days = [DailyAnalysis.model_validate(a) for a in analyses]

    def peak(attr: str) -> DailyAnalysis:
        return max(days, key=lambda d: getattr(d, attr))

    hottest, windiest = peak("max_temperature"), peak("wind_speed")
    most_humid, rainiest = peak("humidity"), peak("precipitation")

    return "\n".join([
        "Weather Summary:",
        f"Hottest day: {hottest.date} with a maximum temperature of {hottest.max_temperature:.1f}°C",
        f"Windiest day: {windiest.date} with wind speeds of {windiest.wind_speed:.1f} km/h",
        f"Most humid day: {most_humid.date} with a humidity level of {most_humid.humidity}%",
        f"Rainiest day: {rainiest.date} with {rainiest.precipitation:.1f} mm of precipitation"
        if rainiest.is_rainy_day else "Rainiest day: none (no precipitation recorded)",
    ])


if __name__ == "__main__":
    setup_logging()
    try:
        report = WeatherReport.model_validate(load_json(data_path("tokyo_weather_complex.json")))
        logger.info("City: %s (%s, %s), timezone: %s",
                    report.city, report.latitude, report.longitude, report.timezone)

        analyses = [analyze_daily_weather(day.model_dump()) for day in report.daily]
        for analysis in analyses:
            logger.info("Daily report:\n%s", generate_daily_report(analysis))

        logger.info("%s", summarize_weather_analysis(analyses))
    except Exception:
        logger.exception("Task 3 failed")
