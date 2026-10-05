"""Irrigation need calculation and weather adjustment pure functions."""

from __future__ import annotations


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
