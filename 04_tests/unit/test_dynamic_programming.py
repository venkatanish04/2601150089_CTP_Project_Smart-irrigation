"""Unit tests for the Dynamic Programming 0/1 knapsack scheduler."""

import pytest
from app.algorithms.dynamic_programming import dynamic_schedule
from app.models.irrigation import Candidate


def test_dp_finds_exact_optimum() -> None:
    # Classic knapsack where Greedy fails:
    # A: 10L, value 60 (ratio 6)
    # B: 20L, value 100 (ratio 5)
    # C: 30L, value 120 (ratio 4)
    # Budget 50L.
    # Greedy picks A + B = 30L, value 160.
    # DP picks B + C = 50L, value 220.
    items = [
        Candidate("A", 10, 60.0, 0.0, "r"),
        Candidate("B", 20, 100.0, 0.0, "r"),
        Candidate("C", 30, 120.0, 0.0, "r"),
    ]
    chosen = dynamic_schedule(items, 50)
    assert [c.field_id for c in chosen] == ["B", "C"]
    assert sum(c.benefit for c in chosen) == 220.0
    assert sum(c.water for c in chosen) == 50


def test_dp_empty_candidates() -> None:
    assert dynamic_schedule([], 50) == []


def test_dp_zero_budget() -> None:
    items = [Candidate("A", 10, 60.0, 0.0, "r")]
    assert dynamic_schedule(items, 0) == []


def test_dp_negative_budget_raises() -> None:
    with pytest.raises(ValueError, match="budget"):
        dynamic_schedule([], -10)
