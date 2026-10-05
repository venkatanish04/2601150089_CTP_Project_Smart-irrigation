"""Benefit scoring and decision rationale description."""

from __future__ import annotations

from app.core.priority import calculate_priority


def calculate_benefit(
    moisture: float, threshold: float, priority: int, rain_probability: float
) -> float:
    """Value of irrigating a field: urgency scaled by 100 and the no-rain chance."""
    urgency = calculate_priority(moisture, threshold, priority)
    return urgency * 100 * (1 - rain_probability / 100)


def describe_reason(moisture: float, threshold: float) -> str:
    """Classify the urgency severity level for user explanation."""
    ratio = (threshold - moisture) / threshold
    if ratio >= 0.5:
        return "Critical moisture"
    if ratio >= 0.25:
        return "High moisture deficit"
    return "Moderate deficit"
