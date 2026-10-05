"""Strategy pattern: interchangeable scheduling algorithms."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.algorithms.dynamic_programming import dynamic_schedule
from app.algorithms.greedy import greedy_schedule
from app.models.irrigation import Candidate


class Scheduler(ABC):
    name: str = "abstract"

    @abstractmethod
    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        """Choose which candidates to irrigate within ``budget`` litres."""


class GreedyScheduler(Scheduler):
    name = "Greedy"

    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        return greedy_schedule(candidates, budget)


class DPScheduler(Scheduler):
    name = "Dynamic Programming"

    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        return dynamic_schedule(candidates, budget)
