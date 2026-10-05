"""Property-based testing with Hypothesis verifying formal invariants."""

from itertools import combinations
from hypothesis import given, settings
from hypothesis import strategies as st
from app.algorithms.dynamic_programming import dynamic_schedule
from app.algorithms.greedy import greedy_schedule
from app.models.irrigation import Candidate

# Strategy generating random candidates
candidates_strategy = st.lists(
    st.tuples(st.integers(1, 30), st.floats(0.0, 300.0)), min_size=0, max_size=10
).map(lambda pairs: [Candidate(f"F{i}", w, b, 0.0, "reason") for i, (w, b) in enumerate(pairs)])

budget_strategy = st.integers(0, 200)


@given(candidates_strategy, budget_strategy)
def test_greedy_always_respects_budget(cands: list[Candidate], budget: int) -> None:
    scheduled = greedy_schedule(cands, budget)
    assert sum(c.water for c in scheduled) <= budget


@given(candidates_strategy, budget_strategy)
def test_dp_always_respects_budget(cands: list[Candidate], budget: int) -> None:
    scheduled = dynamic_schedule(cands, budget)
    assert sum(c.water for c in scheduled) <= budget


@given(candidates_strategy, budget_strategy)
def test_dp_benefit_greater_than_or_equal_to_greedy(cands: list[Candidate], budget: int) -> None:
    greedy_val = sum(c.benefit for c in greedy_schedule(cands, budget))
    dp_val = sum(c.benefit for c in dynamic_schedule(cands, budget))
    assert dp_val >= greedy_val - 1e-6


@settings(max_examples=40)
@given(
    st.lists(st.tuples(st.integers(1, 15), st.integers(0, 80)), min_size=0, max_size=6),
    st.integers(0, 40),
)
def test_dp_matches_exhaustive_brute_force(pairs: list[tuple[int, int]], budget: int) -> None:
    cands = [Candidate(f"F{i}", w, float(b), 0.0, "r") for i, (w, b) in enumerate(pairs)]
    best_value = 0.0
    for r in range(len(cands) + 1):
        for combo in combinations(cands, r):
            if sum(c.water for c in combo) <= budget:
                best_value = max(best_value, sum(c.benefit for c in combo))
    dp_result = sum(c.benefit for c in dynamic_schedule(cands, budget))
    assert abs(dp_result - best_value) < 1e-6
