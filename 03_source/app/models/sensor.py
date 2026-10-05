"""Sensor reading model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SoilReading:
    field_id: str
    moisture: float  # %
    temperature: float  # degrees C
    timestamp: datetime
