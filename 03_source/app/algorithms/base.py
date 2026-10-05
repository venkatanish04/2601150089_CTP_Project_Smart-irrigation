"""Base interface and typing for scheduling algorithms."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from app.models.irrigation import Candidate

# Protocol representing any scheduling algorithm function
SchedulerFunction = Callable[[list[Candidate], int], list[Candidate]]
