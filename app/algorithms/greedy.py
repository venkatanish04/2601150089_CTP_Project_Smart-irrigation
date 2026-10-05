"""Greedy scheduler: best benefit-per-litre first. O(n log n) time, O(n) space."""

from __future__ import annotations

from app.models.irrigation import Candidate
from app.utils.timing import measure_time


@measure_time
def greedy_schedule(candidates: list[Candidate], budget: int) -> list[Candidate]:
    if budget < 0:
        raise ValueError("budget must not be negative")
    ranked = sorted(candidates, key=lambda c: c.benefit / c.water, reverse=True)
    selected: list[Candidate] = []
    remaining = budget
    for candidate in ranked:
        if candidate.water <= remaining:
            selected.append(candidate)
            remaining -= candidate.water
    return selected
