"""Schedule validation logic."""

from __future__ import annotations

from app.models.irrigation import Schedule


def validate_schedule(schedule: Schedule) -> None:
    """Validate budget compliance, positive water allocations, and uniqueness."""
    schedule.validate()
