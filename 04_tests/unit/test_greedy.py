"""Unit tests for the Greedy scheduling algorithm."""

import pytest
from app.algorithms.greedy import greedy_schedule
from app.models.irrigation import Candidate


def test_greedy_schedule_basic() -> None:
    cands = [
        Candidate("F1", 10, 50.0, 10.0, "reason1"),  # ratio 5.0
        Candidate("F2", 20, 80.0, 10.0, "reason2"),  # ratio 4.0
        Candidate("F3", 15, 90.0, 10.0, "reason3"),  # ratio 6.0
    ]
    # Sorted by ratio: F3 (6.0, 15L), F1 (5.0, 10L), F2 (4.0, 20L)
    # Budget 25: picks F3 (15L) + F1 (10L) = 25L
    selected = greedy_schedule(cands, 25)
    assert [c.field_id for c in selected] == ["F3", "F1"]
    assert sum(c.water for c in selected) == 25


def test_greedy_zero_budget() -> None:
    cands = [Candidate("F1", 10, 50.0, 10.0, "reason1")]
    assert greedy_schedule(cands, 0) == []


def test_greedy_negative_budget_raises() -> None:
    with pytest.raises(ValueError, match="budget"):
        greedy_schedule([], -5)
