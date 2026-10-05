"""Weather forecast model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherForecast:
    rainfall_probability: float  # 0..100 %
    temperature: float  # degrees C
    rainfall_mm: float
