"""Monitoring helpers: heap-based urgency queue and active-field tracking."""

from __future__ import annotations

import heapq
from collections.abc import Iterable

from app.models.irrigation import Candidate


class UrgentQueue:
    """Max-priority queue (heapq is a min-heap, so benefits are negated)."""

    def __init__(self, candidates: Iterable[Candidate] = ()) -> None:
        self._heap: list[tuple[float, str]] = []
        for c in candidates:
            self.push(c)

    def push(self, candidate: Candidate) -> None:
        heapq.heappush(self._heap, (-candidate.benefit, candidate.field_id))

    def pop(self) -> str:
        return heapq.heappop(self._heap)[1]

    def __len__(self) -> int:
        return len(self._heap)


def active_fields(candidates: Iterable[Candidate]) -> set[str]:
    """Set of field ids that currently need water."""
    return {c.field_id for c in candidates}


def moisture_map(candidates: Iterable[Candidate]) -> dict[str, float]:
    return {c.field_id: c.moisture for c in candidates}
