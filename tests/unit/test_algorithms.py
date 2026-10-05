import pytest

from app.algorithms.dynamic_programming import dynamic_schedule
from app.algorithms.greedy import greedy_schedule
from app.models.irrigation import Candidate
from app.scheduler.scheduler import DPScheduler, GreedyScheduler, Scheduler


def total(sel: list[Candidate]) -> tuple[int, float]:
    return sum(c.water for c in sel), sum(c.benefit for c in sel)


@pytest.mark.parametrize("algo", [greedy_schedule, dynamic_schedule])
def test_edge_cases(algo, candidates) -> None:  # type: ignore[no-untyped-def]
    assert algo(candidates, 0) == []
    assert algo([], 100) == []
    assert algo(candidates[:1], 100) == candidates[:1]
    assert len(algo(candidates, 10_000)) == len(candidates)
    with pytest.raises(ValueError):
        algo(candidates, -1)


def test_item_that_does_not_fit_is_skipped(candidates) -> None:  # type: ignore[no-untyped-def]
    assert greedy_schedule(candidates[1:2], 39) == []
    assert dynamic_schedule(candidates[1:2], 39) == []


def test_dp_beats_greedy_on_classic_case() -> None:
    items = [
        Candidate("A", 10, 60.0, 0, "r"),
        Candidate("B", 20, 100.0, 0, "r"),
        Candidate("C", 30, 120.0, 0, "r"),
    ]
    g = total(greedy_schedule(items, 50))
    d = total(dynamic_schedule(items, 50))
    assert g == (30, 160.0)  # A + B by ratio
    assert d == (50, 220.0)  # B + C is optimal
    assert d[1] > g[1]


def test_strategy_pattern_polymorphism(candidates) -> None:  # type: ignore[no-untyped-def]
    for strategy in (GreedyScheduler(), DPScheduler()):
        assert isinstance(strategy, Scheduler)
        chosen = strategy.generate_schedule(candidates, 50)
        assert total(chosen)[0] <= 50
        assert strategy.name != "abstract"


def test_abstract_scheduler_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Scheduler()  # type: ignore[abstract]
