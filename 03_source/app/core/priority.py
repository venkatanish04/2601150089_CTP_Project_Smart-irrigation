"""Priority calculation based on soil moisture deficit and field weight."""

from __future__ import annotations


def calculate_priority(moisture: float, threshold: float, priority: int) -> float:
    """Urgency = deficit ratio x field priority (0 when moisture is sufficient)."""
    if moisture >= threshold:
        return 0.0
    return ((threshold - moisture) / threshold) * priority
