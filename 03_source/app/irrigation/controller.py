"""Irrigation controller and valve actuation simulator."""

from __future__ import annotations

import logging
from app.models.irrigation import Schedule, ScheduleEntry

logger = logging.getLogger(__name__)


class IrrigationController:
    """Simulates physical valve opening, duration timing, and execution tracking."""

    def __init__(self) -> None:
        self.active_valves: set[str] = set()
        self.executed_entries: list[ScheduleEntry] = []

    def execute_plan(self, schedule: Schedule) -> list[str]:
        """Simulate sending actuation signals to field solenoid valves."""
        logs: list[str] = []
        schedule.validate()
        for entry in schedule.entries:
            self.active_valves.add(entry.field_id)
            msg = (
                f"Valve OPEN: Field {entry.field_id} | "
                f"Volume {entry.water} L | Start {entry.start:%H:%M} | Reason: {entry.reason}"
            )
            logs.append(msg)
            logger.info(msg)
            self.executed_entries.append(entry)
            self.active_valves.remove(entry.field_id)
        return logs
