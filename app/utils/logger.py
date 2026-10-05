"""Logging setup and a context manager that appends schedules to a log file."""

from __future__ import annotations

import logging
from datetime import datetime
from types import TracebackType
from typing import TextIO

from app.models.irrigation import Schedule


def setup_logging(level: int = logging.WARNING) -> None:
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


class ScheduleLogger:
    """Context manager guaranteeing the log file is closed, even on errors."""

    def __init__(self, path: str = "schedule.log") -> None:
        self.path = path
        self._file: TextIO | None = None

    def __enter__(self) -> ScheduleLogger:
        self._file = open(self.path, "a", encoding="utf-8")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

    def write(self, schedule: Schedule) -> None:
        if self._file is None:
            raise RuntimeError("ScheduleLogger must be used in a 'with' block")
        stamp = datetime.now().isoformat(timespec="seconds")
        self._file.write(
            f"{stamp} {schedule.algorithm} water={schedule.total_water}/"
            f"{schedule.budget} benefit={schedule.total_benefit:.2f} "
            f"fields={[e.field_id for e in schedule.entries]}\n"
        )
