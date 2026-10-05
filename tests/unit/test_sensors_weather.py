import asyncio
import time

import pytest

from app.models.field import Field
from app.models.sensor import SoilReading
from app.sensors.manager import SensorManager, SensorReadingIterator, critical_readings
from app.sensors.simulator import FailingSensor, SimulatedSensor, build_simulated_sensors
from app.weather.service import SimulatedWeatherService

FAST = (0.001, 0.003)


def test_simulated_sensor_reading_in_range() -> None:
    r = asyncio.run(SimulatedSensor("F1", delay_range=FAST, seed=1).read())
    assert r.field_id == "F1" and 10 <= r.moisture <= 80


def test_sensor_with_baseline_stays_near_baseline() -> None:
    r = asyncio.run(SimulatedSensor("F1", base_moisture=20, jitter=1, delay_range=FAST).read())
    assert 19 <= r.moisture <= 21


def test_sensor_is_deterministic_with_seed() -> None:
    a = asyncio.run(SimulatedSensor("F", delay_range=FAST, seed=7).read())
    b = asyncio.run(SimulatedSensor("F", delay_range=FAST, seed=7).read())
    assert a.moisture == b.moisture


def test_concurrent_polling_is_faster_than_sequential() -> None:
    fields = [Field(f"F{i}", 1, "x", 35, 10, 3) for i in range(20)]
    mgr = SensorManager(build_simulated_sensors(fields, delay_range=(0.02, 0.02)))
    t0 = time.perf_counter()
    asyncio.run(mgr.collect_sequential())
    seq = time.perf_counter() - t0
    t0 = time.perf_counter()
    out = asyncio.run(mgr.collect_readings())
    conc = time.perf_counter() - t0
    assert len(out) == 20
    assert conc < seq / 3


def test_failing_sensor_does_not_break_collection() -> None:
    mgr = SensorManager([SimulatedSensor("A", delay_range=FAST), FailingSensor("B")])
    assert set(asyncio.run(mgr.collect_readings())) == {"A"}
    assert set(asyncio.run(mgr.collect_sequential())) == {"A"}


def test_slow_sensor_times_out() -> None:
    mgr = SensorManager([SimulatedSensor("A", delay_range=(0.5, 0.5))], timeout=0.01)
    assert asyncio.run(mgr.collect_readings()) == {}


def test_stream_yields_all_readings() -> None:
    mgr = SensorManager([SimulatedSensor(x, delay_range=FAST) for x in "ABC"])

    async def collect() -> list[SoilReading]:
        return [r async for r in mgr.stream()]

    assert {r.field_id for r in asyncio.run(collect())} == {"A", "B", "C"}


def test_iterator_and_generator() -> None:
    mgr = SensorManager(
        [SimulatedSensor(x, base_moisture=m, delay_range=FAST) for x, m in (("A", 10), ("B", 60))]
    )
    readings = list(asyncio.run(mgr.collect_readings()).values())
    assert [r.field_id for r in SensorReadingIterator(readings)] == ["A", "B"]
    assert [r.field_id for r in critical_readings(readings, 30)] == ["A"]
    it = SensorReadingIterator([])
    with pytest.raises(StopIteration):
        next(it)


def test_weather_service() -> None:
    f = asyncio.run(SimulatedWeatherService(25, seed=1, delay=0.001).get_forecast())
    assert f.rainfall_probability == 25
    g = asyncio.run(SimulatedWeatherService(seed=1, delay=0.001).get_forecast())
    assert 0 <= g.rainfall_probability <= 100
