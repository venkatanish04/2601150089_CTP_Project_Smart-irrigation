"""Unit tests for sensor models, simulator, and iterator."""

import asyncio
from datetime import datetime
import pytest
from app.models.sensor import SoilReading
from app.sensors.manager import SensorReadingIterator
from app.sensors.simulator import FailingSensor, SimulatedSensor


def test_soil_reading_valid() -> None:
    now = datetime.now()
    r = SoilReading("F01", 25.5, 30.0, now)
    assert r.field_id == "F01"
    assert r.moisture == 25.5
    assert r.temperature == 30.0
    assert r.timestamp == now


def test_sensor_iterator() -> None:
    now = datetime.now()
    readings = [SoilReading("F01", 20.0, 25.0, now), SoilReading("F02", 30.0, 26.0, now)]
    it = SensorReadingIterator(readings)
    assert iter(it) is it
    assert next(it).field_id == "F01"
    assert next(it).field_id == "F02"
    with pytest.raises(StopIteration):
        next(it)


def test_simulated_sensor_read() -> None:
    s = SimulatedSensor("F01", base_moisture=22.0, delay_range=(0.001, 0.002))
    reading = asyncio.run(s.read())
    assert reading.field_id == "F01"
    assert reading.moisture >= 0.0


def test_failing_sensor_raises() -> None:
    s = FailingSensor("F01")
    with pytest.raises(ConnectionError, match="unreachable"):
        asyncio.run(s.read())
