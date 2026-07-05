"""Tests for Weather Service."""

from backend.modules.weather.service import WeatherService, WEATHER_EMOJIS


class TestWeatherService:
    def test_init(self):
        svc = WeatherService()
        assert svc is not None

    def test_weather_emojis(self):
        assert WEATHER_EMOJIS["clear"] == "☀️"
        assert WEATHER_EMOJIS["rain"] == "🌧️"
        assert WEATHER_EMOJIS["snow"] == "❄️"
        assert "unknown" not in WEATHER_EMOJIS
        assert WEATHER_EMOJIS.get("unknown", "🌡️") == "🌡️"

    def test_format_weather_response(self):
        svc = WeatherService()
        from backend.modules.weather.service import WeatherData
        from datetime import datetime
        w = WeatherData(
            condition="clear", description="clear sky", temperature=28.5,
            feels_like=26.0, humidity=45, wind_speed=3.2,
            icon="01d", emoji="☀️", city="New Delhi",
            country="IN", sunrise=datetime.now(), sunset=datetime.now(),
        )
        response = svc.format_weather_response(w)
        assert "28" in response
        assert "New Delhi" in response
        assert "clear sky" in response
        assert "☀️" in response
