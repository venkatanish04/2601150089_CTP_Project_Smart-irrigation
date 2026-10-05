"""Sensor abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.sensor import SoilReading


class Sensor(ABC):
    field_id: str

    @abstractmethod
    async def read(self) -> SoilReading:
        """Take one reading (I/O-bound: awaits the device)."""
