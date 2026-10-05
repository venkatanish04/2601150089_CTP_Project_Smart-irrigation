"""Field model: static configuration of one irrigation zone."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    field_id: str
    area: float  # square metres
    crop: str
    moisture_threshold: float  # % below which the field needs water
    water_requirement: float  # litres for a full irrigation cycle
    priority: int  # 1 (low) .. 5 (critical)

    def __post_init__(self) -> None:
        if not 0 < self.moisture_threshold <= 100:
            raise ValueError("moisture_threshold must be in (0, 100]")
        if self.water_requirement <= 0:
            raise ValueError("water_requirement must be positive")
        if not 1 <= self.priority <= 5:
            raise ValueError("priority must be between 1 and 5")
        if self.area <= 0:
            raise ValueError("area must be positive")
