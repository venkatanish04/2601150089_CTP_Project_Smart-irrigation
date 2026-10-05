"""Default configuration and demo field data."""

from __future__ import annotations

from dataclasses import dataclass

from app.models.field import Field

DEFAULT_FIELDS: list[Field] = [
    Field("F01", 1000, "Rice", 35, 30, 4),
    Field("F02", 800, "Wheat", 35, 20, 1),
    Field("F03", 1200, "Maize", 35, 35, 4),
    Field("F04", 900, "Cotton", 35, 25, 3),
    Field("F05", 1500, "Sugarcane", 35, 40, 5),
]

# Starting soil-moisture profile for the demo (%), from the project blueprint.
DEMO_MOISTURE: dict[str, float] = {
    "F01": 18,
    "F02": 42,
    "F03": 21,
    "F04": 35,
    "F05": 15,
}


@dataclass(frozen=True)
class Settings:
    water_budget: int = 40
    slot_minutes: int = 20
    start_hour: int = 6
    sensor_timeout: float = 2.0
    demo_rain_probability: float = 10.0
