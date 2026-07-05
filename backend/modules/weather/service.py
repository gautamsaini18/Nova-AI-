"""Nova AI — Weather Service

Provides current weather, forecasts, and alerts
via OpenWeatherMap API.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import httpx

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("weather.service")

WEATHER_EMOJIS = {
    "clear": "☀️", "clouds": "☁️", "rain": "🌧️", "drizzle": "🌦️",
    "thunderstorm": "⛈️", "snow": "❄️", "mist": "🌫️", "fog": "🌫️",
    "haze": "🌫️", "dust": "💨", "smoke": "💨",
}


@dataclass
class WeatherData:
    condition: str
    description: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    icon: str
    emoji: str
    city: str
    country: str
    sunrise: datetime
    sunset: datetime


@dataclass
class ForecastDay:
    date: str
    temp_high: float
    temp_low: float
    condition: str
    description: str
    emoji: str
    humidity: int
    wind_speed: float


class WeatherService:
    """Fetches weather data from OpenWeatherMap."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self) -> None:
        self._api_key = settings.OPENWEATHER_API_KEY
        self._default_city = settings.DEFAULT_CITY
        self._default_country = settings.DEFAULT_COUNTRY_CODE
        logger.info("WeatherService initialized")

    async def get_current_weather(self, city: Optional[str] = None) -> Optional[WeatherData]:
        """Get current weather for a city."""
        location = city or self._default_city
        if not self._api_key:
            logger.warning("OpenWeatherMap API key not set")
            return None

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.BASE_URL}/weather",
                    params={"q": location, "appid": self._api_key, "units": "metric"},
                )
                resp.raise_for_status()
                data = resp.json()
                w = data["weather"][0]
                condition = w["main"].lower()
                return WeatherData(
                    condition=condition,
                    description=w["description"],
                    temperature=data["main"]["temp"],
                    feels_like=data["main"]["feels_like"],
                    humidity=data["main"]["humidity"],
                    wind_speed=data["wind"]["speed"],
                    icon=w["icon"],
                    emoji=WEATHER_EMOJIS.get(condition, "🌡️"),
                    city=data["name"],
                    country=data["sys"].get("country", ""),
                    sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]),
                    sunset=datetime.fromtimestamp(data["sys"]["sunset"]),
                )
        except Exception as exc:
            logger.error("Failed to fetch weather", error=str(exc))
            return None

    async def get_forecast(self, city: Optional[str] = None, days: int = 5) -> list[ForecastDay]:
        """Get weather forecast for the next N days."""
        location = city or self._default_city
        if not self._api_key:
            return []

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{self.BASE_URL}/forecast",
                    params={"q": location, "appid": self._api_key, "units": "metric", "cnt": days * 8},
                )
                resp.raise_for_status()
                data = resp.json()
                forecasts: list[ForecastDay] = []
                seen_dates: set[str] = set()
                for entry in data["list"]:
                    date = entry["dt_txt"].split()[0]
                    if date in seen_dates:
                        continue
                    seen_dates.add(date)
                    w = entry["weather"][0]
                    condition = w["main"].lower()
                    forecasts.append(ForecastDay(
                        date=date,
                        temp_high=entry["main"]["temp_max"],
                        temp_low=entry["main"]["temp_min"],
                        condition=condition,
                        description=w["description"],
                        emoji=WEATHER_EMOJIS.get(condition, "🌡️"),
                        humidity=entry["main"]["humidity"],
                        wind_speed=entry["wind"]["speed"],
                    ))
                    if len(forecasts) >= days:
                        break
                return forecasts
        except Exception as exc:
            logger.error("Failed to fetch forecast", error=str(exc))
            return []

    def format_weather_response(self, weather: WeatherData) -> str:
        """Format weather data into a natural language response."""
        return (
            f"It's currently {weather.temperature:.0f}°C in {weather.city} "
            f"with {weather.description}. Feels like {weather.feels_like:.0f}°C. "
            f"Humidity is at {weather.humidity}% and wind speed is {weather.wind_speed} m/s. "
            f"{weather.emoji}"
        )
