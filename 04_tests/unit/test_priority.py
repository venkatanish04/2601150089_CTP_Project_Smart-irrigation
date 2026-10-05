"""Unit tests for field priority and benefit scoring pure functions."""

import pytest
from app.algorithms.scoring import calculate_benefit, calculate_priority, describe_reason


def test_priority_calculation() -> None:
    # moisture 10%, threshold 40%, priority 5 -> deficit ratio 0.75 * 5 = 3.75
    p = calculate_priority(10.0, 40.0, 5)
    assert abs(p - 3.75) < 1e-6


def test_priority_when_moisture_sufficient() -> None:
    assert calculate_priority(40.0, 40.0, 5) == 0.0
    assert calculate_priority(45.0, 40.0, 5) == 0.0


def test_benefit_calculation_with_weather() -> None:
    # priority 3.75 * 100 * (1 - 0.20 rain) = 375 * 0.8 = 300.0
    b = calculate_benefit(10.0, 40.0, 5, 20.0)
    assert abs(b - 300.0) < 1e-6


def test_describe_reason_classifications() -> None:
    assert describe_reason(10.0, 40.0) == "Critical moisture"  # ratio 0.75 >= 0.5
    assert describe_reason(25.0, 40.0) == "High moisture deficit"  # ratio 0.375 >= 0.25
    assert describe_reason(35.0, 40.0) == "Moderate deficit"  # ratio 0.125 < 0.25
