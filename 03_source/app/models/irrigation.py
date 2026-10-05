"""Models describing irrigation candidates and generated schedules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Candidate:
    """A field that needs water: weight = litres, value = benefit."""

    field_id: str
    water: int  # litres (integer so DP can index on it)
    benefit: float
    moisture: float
    reason: str


@dataclass(frozen=True)
class ScheduleEntry:
    order: int
    field_id: str
    water: int
    start: datetime
    reason: str


@dataclass
class Schedule:
    algorithm: str
    budget: int
    entries: list[ScheduleEntry] = field(default_factory=list)
    total_benefit: float = 0.0
    elapsed: float = 0.0  # seconds spent in the scheduling algorithm

    @property
    def total_water(self) -> int:
        return sum(e.water for e in self.entries)

    @property
    def unused_water(self) -> int:
        return self.budget - self.total_water

    def validate(self) -> None:
        if self.total_water > self.budget:
            raise ValueError(f"schedule uses {self.total_water} L but budget is {self.budget} L")
