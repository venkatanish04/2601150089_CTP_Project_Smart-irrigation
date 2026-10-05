"""Property-based tests (Hypothesis)."""

from itertools import combinations

from hypothesis import given, settings
from hypothesis import strategies as st

from app.algorithms.dynamic_programming import dynamic_schedule
from app.algorithms.greedy import greedy_schedule
from app.algorithms.scoring import calculate_irrigation_need, weather_adjustment
from app.models.irrigation import Candidate

items = st.lists(st.tuples(st.integers(1, 40), st.floats(0.0, 500.0)), min_size=0, max_size=12).map(
    lambda rows: [Candidate(f"F{i}", w, v, 10.0, "r") for i, (w, v) in enumerate(rows)]
)
budgets = st.integers(0, 300)


def water(sel: list[Candidate]) -> int:
    return sum(c.water for c in sel)


def benefit(sel: list[Candidate]) -> float:
    return sum(c.benefit for c in sel)


@given(items, budgets)
def test_greedy_never_exceeds_budget(cands: list[Candidate], budget: int) -> None:
    assert water(greedy_schedule(cands, budget)) <= budget


@given(items, budgets)
def test_dp_never_exceeds_budget(cands: list[Candidate], budget: int) -> None:
    assert water(dynamic_schedule(cands, budget)) <= budget


@given(items, budgets)
def test_dp_at_least_as_good_as_greedy(cands: list[Candidate], budget: int) -> None:
    assert (
        benefit(dynamic_schedule(cands, budget)) >= benefit(greedy_schedule(cands, budget)) - 1e-6
    )


@given(items, budgets)
def test_no_duplicate_fields(cands: list[Candidate], budget: int) -> None:
    for algo in (greedy_schedule, dynamic_schedule):
        ids = [c.field_id for c in algo(cands, budget)]
        assert len(ids) == len(set(ids))


@settings(max_examples=60)
@given(st.lists(st.tuples(st.integers(1, 20), st.integers(0, 100)), max_size=8), st.integers(0, 60))
def test_dp_matches_brute_force(rows: list[tuple[int, int]], budget: int) -> None:
    cands = [Candidate(f"F{i}", w, float(v), 0, "r") for i, (w, v) in enumerate(rows)]
    best = 0.0
    for r in range(len(cands) + 1):
        for combo in combinations(cands, r):
            if water(list(combo)) <= budget:
                best = max(best, benefit(list(combo)))
    assert abs(benefit(dynamic_schedule(cands, budget)) - best) < 1e-9


@given(st.floats(0, 100), st.floats(1, 100), st.floats(0, 500))
def test_need_bounds(moisture: float, threshold: float, req: float) -> None:
    need = calculate_irrigation_need(moisture, threshold, req)
    assert 0 <= need <= req


@given(st.floats(0, 1000), st.floats(0, 100))
def test_rain_never_increases_water(water_req: float, rain: float) -> None:
    assert weather_adjustment(water_req, rain) <= water_req
