"""Integration tests for sensor telemetry acquisition and fault isolation."""

import asyncio
from app.sensors.manager import SensorManager
from app.sensors.simulator import FailingSensor, SimulatedSensor


def test_sensor_manager_collects_concurrently() -> None:
    sensors = [
        SimulatedSensor("F01", base_moisture=20.0, delay_range=(0.001, 0.002)),
        SimulatedSensor("F02", base_moisture=35.0, delay_range=(0.001, 0.002)),
    ]
    mgr = SensorManager(sensors, timeout=1.0)
    readings = asyncio.run(mgr.collect_readings())
    assert len(readings) == 2
    assert "F01" in readings
    assert "F02" in readings


def test_failing_sensor_is_isolated_gracefully() -> None:
    sensors = [
        SimulatedSensor("F01", base_moisture=20.0, delay_range=(0.001, 0.002)),
        FailingSensor("F02"),
    ]
    mgr = SensorManager(sensors, timeout=1.0)
    readings = asyncio.run(mgr.collect_readings())
    assert "F01" in readings
    assert "F02" not in readings
