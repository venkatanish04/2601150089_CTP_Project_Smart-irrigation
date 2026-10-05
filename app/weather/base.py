"""Weather service base interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.weather import WeatherForecast


class WeatherService(ABC):
    @abstractmethod
    async def get_forecast(self) -> WeatherForecast: ...
