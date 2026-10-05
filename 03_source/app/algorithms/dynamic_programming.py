"""0/1 knapsack DP scheduler. O(nW) time, O(nW) space (table kept for reconstruction)."""

from __future__ import annotations

from app.models.irrigation import Candidate
from app.utils.timing import measure_time


@measure_time
def dynamic_schedule(candidates: list[Candidate], budget: int) -> list[Candidate]:
    """dp[i][w] = best benefit using the first i candidates with w litres."""
    if budget < 0:
        raise ValueError("budget must not be negative")
    n = len(candidates)
    dp = [[0.0] * (budget + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        cand = candidates[i - 1]
        for w in range(budget + 1):
            best = dp[i - 1][w]
            if cand.water <= w:
                best = max(best, cand.benefit + dp[i - 1][w - cand.water])
            dp[i][w] = best
    return _reconstruct(dp, candidates, budget)


def _reconstruct(
    dp: list[list[float]], candidates: list[Candidate], budget: int
) -> list[Candidate]:
    chosen: list[Candidate] = []
    w = budget
    for i in range(len(candidates), 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # candidate i-1 was taken
            cand = candidates[i - 1]
            chosen.append(cand)
            w -= cand.water
    chosen.reverse()
    return chosen
