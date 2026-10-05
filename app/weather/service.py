"""Weather abstraction with a simulated implementation."""

from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod

from app.models.weather import WeatherForecast


class WeatherService(ABC):
    @abstractmethod
    async def get_forecast(self) -> WeatherForecast: ...


class SimulatedWeatherService(WeatherService):
    def __init__(
        self,
        rain_probability: float | None = None,
        seed: int | None = None,
        delay: float = 0.1,
    ) -> None:
        self.rain_probability = rain_probability
        self.delay = delay
        self._rng = random.Random(seed)

    async def get_forecast(self) -> WeatherForecast:
        await asyncio.sleep(self.delay)
        rain = (
            self.rain_probability
            if self.rain_probability is not None
            else self._rng.uniform(0, 100)
        )
        return WeatherForecast(
            rainfall_probability=round(rain, 1),
            temperature=round(self._rng.uniform(25, 38), 1),
            rainfall_mm=round(rain / 100 * self._rng.uniform(0, 12), 1),
        )
