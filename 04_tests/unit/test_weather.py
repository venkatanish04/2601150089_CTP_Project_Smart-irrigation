"""Unit tests for weather forecasting models and services."""

import asyncio
from app.models.weather import WeatherForecast
from app.weather.simulator import SimulatedWeatherService


def test_weather_forecast_valid() -> None:
    f = WeatherForecast(15.0, 32.0, 2.5)
    assert f.rainfall_probability == 15.0
    assert f.temperature == 32.0
    assert f.rainfall_mm == 2.5


def test_simulated_weather_service() -> None:
    service = SimulatedWeatherService(rain_probability=20.0, delay=0.001)
    f = asyncio.run(service.get_forecast())
    assert f.rainfall_probability == 20.0
    assert f.temperature > 0.0
