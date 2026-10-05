"""Pure functions for irrigation need, weather adjustment and benefit scoring."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping

from app.models.field import Field
from app.models.irrigation import Candidate
from app.models.sensor import SoilReading
from app.models.weather import WeatherForecast


def calculate_irrigation_need(moisture: float, threshold: float, water_requirement: float) -> float:
    """Litres needed, proportional to the moisture deficit. Zero if moist enough."""
    if moisture < 0 or moisture > 100:
        raise ValueError("moisture must be between 0 and 100")
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    if water_requirement < 0:
        raise ValueError("water_requirement must not be negative")
    if moisture >= threshold:
        return 0.0
    deficit = threshold - moisture
    return water_requirement * (deficit / threshold)


def weather_adjustment(water_required: float, rain_probability: float) -> float:
    """Reduce the requirement by the chance of rain (0..100 %)."""
    if not 0 <= rain_probability <= 100:
        raise ValueError("rain_probability must be between 0 and 100")
    return water_required * (1 - rain_probability / 100)


def calculate_priority(moisture: float, threshold: float, priority: int) -> float:
    """Urgency = deficit ratio x field priority (0 when moisture is sufficient)."""
    if moisture >= threshold:
        return 0.0
    return ((threshold - moisture) / threshold) * priority


def calculate_benefit(
    moisture: float, threshold: float, priority: int, rain_probability: float
) -> float:
    """Value of irrigating a field: urgency scaled by 100 and the no-rain chance."""
    urgency = calculate_priority(moisture, threshold, priority)
    return urgency * 100 * (1 - rain_probability / 100)


def describe_reason(moisture: float, threshold: float) -> str:
    ratio = (threshold - moisture) / threshold
    if ratio >= 0.5:
        return "Critical moisture"
    if ratio >= 0.25:
        return "High moisture deficit"
    return "Moderate deficit"


def build_candidates(
    fields: Iterable[Field],
    readings: Mapping[str, SoilReading],
    forecast: WeatherForecast,
) -> list[Candidate]:
    """Turn raw readings into irrigation candidates (only fields that need water)."""
    candidates: list[Candidate] = []
    for f in fields:
        reading = readings.get(f.field_id)
        if reading is None:  # sensor failed: skip rather than guess
            continue
        need = weather_adjustment(
            calculate_irrigation_need(reading.moisture, f.moisture_threshold, f.water_requirement),
            forecast.rainfall_probability,
        )
        litres = math.ceil(need)
        if litres <= 0:
            continue
        benefit = calculate_benefit(
            reading.moisture,
            f.moisture_threshold,
            f.priority,
            forecast.rainfall_probability,
        )
        candidates.append(
            Candidate(
                field_id=f.field_id,
                water=litres,
                benefit=benefit,
                moisture=reading.moisture,
                reason=describe_reason(reading.moisture, f.moisture_threshold),
            )
        )
    return candidates
