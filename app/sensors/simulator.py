"""Simulated soil sensors so the system runs without hardware."""

from __future__ import annotations

import asyncio
import random
from collections.abc import Iterable, Mapping
from datetime import datetime

from app.models.field import Field
from app.models.sensor import SoilReading
from app.sensors.base import Sensor


class SimulatedSensor(Sensor):
    def __init__(
        self,
        field_id: str,
        base_moisture: float | None = None,
        jitter: float = 1.5,
        delay_range: tuple[float, float] = (0.1, 0.5),
        seed: int | None = None,
    ) -> None:
        self.field_id = field_id
        self.base_moisture = base_moisture
        self.jitter = jitter
        self.delay_range = delay_range
        self._rng = random.Random(seed)

    async def read(self) -> SoilReading:
        await asyncio.sleep(self._rng.uniform(*self.delay_range))
        if self.base_moisture is None:
            moisture = self._rng.uniform(10, 80)
        else:
            moisture = self.base_moisture + self._rng.uniform(-self.jitter, self.jitter)
        moisture = min(100.0, max(0.0, moisture))
        return SoilReading(
            field_id=self.field_id,
            moisture=round(moisture, 1),
            temperature=round(self._rng.uniform(20, 40), 1),
            timestamp=datetime.now(),
        )


class FailingSensor(Sensor):
    """Sensor that always fails; used to test fault tolerance."""

    def __init__(self, field_id: str) -> None:
        self.field_id = field_id

    async def read(self) -> SoilReading:
        raise ConnectionError(f"sensor {self.field_id} unreachable")


def build_simulated_sensors(
    fields: Iterable[Field],
    profile: Mapping[str, float] | None = None,
    seed: int = 42,
    delay_range: tuple[float, float] = (0.1, 0.5),
) -> list[Sensor]:
    """One simulated sensor per field; each gets its own deterministic seed."""
    return [
        SimulatedSensor(
            f.field_id,
            base_moisture=(profile or {}).get(f.field_id),
            delay_range=delay_range,
            seed=seed + i,
        )
        for i, f in enumerate(fields)
    ]
