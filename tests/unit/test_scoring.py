from datetime import datetime

import pytest

from app.algorithms.scoring import (
    build_candidates,
    calculate_benefit,
    calculate_irrigation_need,
    calculate_priority,
    describe_reason,
    weather_adjustment,
)
from app.models.field import Field
from app.models.sensor import SoilReading
from app.models.weather import WeatherForecast


def test_need_when_moisture_is_low() -> None:
    assert calculate_irrigation_need(20, 40, 40) == 20


def test_need_zero_at_or_above_threshold() -> None:
    assert calculate_irrigation_need(40, 40, 40) == 0
    assert calculate_irrigation_need(70, 40, 40) == 0


def test_need_at_zero_moisture_is_full_requirement() -> None:
    assert calculate_irrigation_need(0, 40, 40) == 40


@pytest.mark.parametrize("args", [(-1, 40, 40), (101, 40, 40), (10, 0, 40), (10, 40, -1)])
def test_need_invalid_inputs(args: tuple[float, float, float]) -> None:
    with pytest.raises(ValueError):
        calculate_irrigation_need(*args)


def test_weather_adjustment() -> None:
    assert weather_adjustment(40, 50) == 20
    assert weather_adjustment(40, 0) == 40
    assert weather_adjustment(40, 100) == 0


def test_weather_adjustment_invalid() -> None:
    with pytest.raises(ValueError):
        weather_adjustment(40, 120)


def test_priority_and_benefit() -> None:
    assert calculate_priority(40, 40, 5) == 0
    assert calculate_priority(20, 40, 4) == pytest.approx(2.0)
    assert calculate_benefit(20, 40, 4, 50) == pytest.approx(100.0)


def test_describe_reason() -> None:
    assert describe_reason(10, 40) == "Critical moisture"
    assert describe_reason(25, 40) == "High moisture deficit"
    assert describe_reason(35, 40) == "Moderate deficit"


def _reading(fid: str, moisture: float) -> SoilReading:
    return SoilReading(fid, moisture, 25.0, datetime(2026, 1, 1))


def test_build_candidates_skips_moist_and_missing() -> None:
    fields = [
        Field("A", 100, "x", 35, 30, 3),
        Field("B", 100, "x", 35, 30, 3),
        Field("C", 100, "x", 35, 30, 3),
    ]
    readings = {"A": _reading("A", 10), "B": _reading("B", 60)}  # C: sensor failed
    result = build_candidates(fields, readings, WeatherForecast(0, 30, 0))
    assert [c.field_id for c in result] == ["A"]
    assert result[0].water == 22  # ceil(30 * 25/35)
