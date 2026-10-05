"""Unit tests for irrigation need calculation and weather adjustment."""

import pytest
from app.algorithms.scoring import calculate_irrigation_need, weather_adjustment


def test_irrigation_need_when_dry() -> None:
    # moisture 20%, threshold 40%, requirement 40L -> deficit 20% -> 20L
    need = calculate_irrigation_need(20.0, 40.0, 40.0)
    assert need == 20.0


def test_irrigation_need_when_saturated() -> None:
    assert calculate_irrigation_need(45.0, 40.0, 40.0) == 0.0
    assert calculate_irrigation_need(40.0, 40.0, 40.0) == 0.0


def test_weather_adjustment_rain_discount() -> None:
    # 40L with 50% rain probability -> 20L
    assert weather_adjustment(40.0, 50.0) == 20.0
    # 0% rain -> 100% need
    assert weather_adjustment(40.0, 0.0) == 40.0
    # 100% rain -> 0L need
    assert weather_adjustment(40.0, 100.0) == 0.0


def test_invalid_parameters_raise() -> None:
    with pytest.raises(ValueError):
        calculate_irrigation_need(-1.0, 40.0, 40.0)
    with pytest.raises(ValueError):
        weather_adjustment(40.0, 120.0)
