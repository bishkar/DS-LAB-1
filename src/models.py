"""
Pydantic models shared by all tasks.

Every piece of data that enters or leaves the scripts (API responses, JSON/XML/text
records, analysis results, CSV rows) is described here once, so validation, type
coercion and CSV headers live in a single place.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


# --------------------------------------------------------------------------- #
# Analysis thresholds (single source of truth for tasks 3 and 4)
# --------------------------------------------------------------------------- #
class Thresholds(BaseModel):
    """Limits used to classify a day."""

    model_config = ConfigDict(frozen=True)

    hot_temperature: float = 30.0         # °C, strictly above -> hot day
    windy_speed: float = 15.0             # km/h, strictly above -> windy day
    uncomfortable_humidity: float = 70.0  # %, strictly above -> uncomfortable
    significant_swing: float = 10.0       # °C, strictly above -> significant swing
    light_rain_max: float = 2.5           # mm, below -> light rain
    moderate_rain_max: float = 7.6        # mm, below -> moderate rain, else heavy


DEFAULT_THRESHOLDS = Thresholds()


def classify_rain(precipitation: float, thresholds: Thresholds = DEFAULT_THRESHOLDS) -> str:
    """
    Classify rain severity based on the daily precipitation amount.

    Args:
        precipitation (float): Precipitation in millimetres.
        thresholds (Thresholds): Rain severity limits.

    Returns:
        str: "none", "light", "moderate" or "heavy".
    """
    if precipitation <= 0:
        return "none"
    if precipitation < thresholds.light_rain_max:
        return "light"
    if precipitation < thresholds.moderate_rain_max:
        return "moderate"
    return "heavy"


# --------------------------------------------------------------------------- #
# Task 1: Wikipedia
# --------------------------------------------------------------------------- #
class WikipediaExtract(BaseModel):
    """Data extracted from a Wikipedia article."""

    title: str
    first_sentence: str


# --------------------------------------------------------------------------- #
# Task 2: Open-Meteo API
# --------------------------------------------------------------------------- #
class OpenMeteoDaily(BaseModel):
    """The `daily` block of an Open-Meteo forecast response."""

    time: List[str]
    temperature_2m_max: List[Optional[float]]


class OpenMeteoResponse(BaseModel):
    """The part of the Open-Meteo forecast response we rely on."""

    daily: OpenMeteoDaily


class TemperatureForecast(BaseModel):
    """Maximum temperature forecast for one day."""

    date: str
    max_temperature: Optional[float]


# --------------------------------------------------------------------------- #
# Tasks 3 and 4: complex weather JSON
# --------------------------------------------------------------------------- #
class DailyWeather(BaseModel):
    """Raw weather observations for a single day."""

    date: str
    max_temperature: float
    min_temperature: float
    precipitation: float = 0.0
    wind_speed: float = 0.0
    humidity: int = 0
    weather_description: str = ""

    @computed_field
    @property
    def temperature_swing(self) -> float:
        return round(self.max_temperature - self.min_temperature, 1)

    @computed_field
    @property
    def is_rainy_day(self) -> bool:
        return self.precipitation > 0

    @computed_field
    @property
    def rain_severity(self) -> str:
        return classify_rain(self.precipitation)

    def analyze(self, thresholds: Thresholds = DEFAULT_THRESHOLDS) -> "DailyAnalysis":
        """Classify the day against the given thresholds."""
        return DailyAnalysis(
            **self.model_dump(include=set(DailyWeather.model_fields)),
            is_hot_day=self.max_temperature > thresholds.hot_temperature,
            is_windy_day=self.wind_speed > thresholds.windy_speed,
            is_uncomfortable_day=self.humidity > thresholds.uncomfortable_humidity,
            is_significant_swing=self.temperature_swing > thresholds.significant_swing,
        )


class DailyAnalysis(DailyWeather):
    """A day of weather together with its classification."""

    is_hot_day: bool
    is_windy_day: bool
    is_uncomfortable_day: bool
    is_significant_swing: Optional[bool] = None

    @model_validator(mode="after")
    def _default_swing_flag(self) -> "DailyAnalysis":
        if self.is_significant_swing is None:
            self.is_significant_swing = self.temperature_swing > DEFAULT_THRESHOLDS.significant_swing
        return self


class WeatherReport(BaseModel):
    """The whole `tokyo_weather_complex.json` file."""

    city: str
    latitude: float
    longitude: float
    timezone: str
    daily: List[DailyWeather]


class WeatherSummary(BaseModel):
    """Key metrics across several days."""

    average_max_temp: float
    average_min_temp: float
    total_precipitation: float
    average_wind_speed: float
    average_humidity: float
    hot_days: int
    windy_days: int
    rainy_days: int


# --------------------------------------------------------------------------- #
# CSV rows: `serialization_alias` is the CSV column header
# --------------------------------------------------------------------------- #
class WeatherCsvRow(BaseModel):
    """Task 4 CSV row."""

    date: str = Field(serialization_alias="Date")
    max_temperature: float = Field(serialization_alias="Max Temperature")
    min_temperature: float = Field(serialization_alias="Min Temperature")
    precipitation: float = Field(serialization_alias="Precipitation")
    wind_speed: float = Field(serialization_alias="Wind Speed")
    humidity: int = Field(serialization_alias="Humidity")
    weather_description: str = Field(serialization_alias="Weather Description")
    is_hot_day: bool = Field(serialization_alias="Is Hot Day")
    is_windy_day: bool = Field(serialization_alias="Is Windy Day")
    is_rainy_day: bool = Field(serialization_alias="Is Rainy Day")


class XmlWeatherDay(BaseModel):
    """Task 5: one <day> element of `weather_data.xml`."""

    date: str = Field(serialization_alias="Date")
    temperature: float = Field(serialization_alias="Temperature")
    humidity: int = Field(serialization_alias="Humidity")
    precipitation: float = Field(serialization_alias="Precipitation")


class TextWeatherDay(BaseModel):
    """Task 6: one line of `weather_report.txt`."""

    date: str = Field(serialization_alias="Date")
    max_temperature: float = Field(serialization_alias="Max Temperature")
    min_temperature: float = Field(serialization_alias="Min Temperature")
    humidity: int = Field(serialization_alias="Humidity")
    precipitation: float = Field(serialization_alias="Precipitation")
