"""Concurrent sensor polling (asyncio), iterator and generator helpers."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator, Iterator, Sequence

from app.models.sensor import SoilReading
from app.sensors.base import Sensor

logger = logging.getLogger(__name__)


class SensorReadingIterator:
    """Hand-written iterator over a list of readings."""

    def __init__(self, readings: Sequence[SoilReading]) -> None:
        self.readings = readings
        self.index = 0

    def __iter__(self) -> Iterator[SoilReading]:
        return self

    def __next__(self) -> SoilReading:
        if self.index >= len(self.readings):
            raise StopIteration
        reading = self.readings[self.index]
        self.index += 1
        return reading


class SensorManager:
    def __init__(self, sensors: Sequence[Sensor], timeout: float = 2.0) -> None:
        self.sensors = list(sensors)
        self.timeout = timeout

    async def _safe_read(self, sensor: Sensor) -> SoilReading | None:
        try:
            return await asyncio.wait_for(sensor.read(), timeout=self.timeout)
        except Exception as exc:  # one bad sensor must not kill the cycle
            logger.warning("sensor %s failed: %r", sensor.field_id, exc)
            return None

    async def collect_readings(self) -> dict[str, SoilReading]:
        """Poll every sensor concurrently."""
        results = await asyncio.gather(*(self._safe_read(s) for s in self.sensors))
        return {r.field_id: r for r in results if r is not None}

    async def collect_sequential(self) -> dict[str, SoilReading]:
        """Baseline: poll one sensor at a time (for the benchmark)."""
        readings: dict[str, SoilReading] = {}
        for sensor in self.sensors:
            result = await self._safe_read(sensor)
            if result is not None:
                readings[result.field_id] = result
        return readings

    async def stream(self) -> AsyncIterator[SoilReading]:
        """Async generator: yield readings as each sensor finishes."""
        tasks = [asyncio.ensure_future(self._safe_read(s)) for s in self.sensors]
        for finished in asyncio.as_completed(tasks):
            result = await finished
            if result is not None:
                yield result


def critical_readings(readings: Sequence[SoilReading], limit: float) -> Iterator[SoilReading]:
    """Generator: lazily yield readings whose moisture is below ``limit``."""
    for reading in readings:
        if reading.moisture < limit:
            yield reading
