import pytest

from app.models.field import Field
from app.models.irrigation import Candidate, Schedule, ScheduleEntry


@pytest.mark.parametrize(
    "kwargs",
    [
        {"moisture_threshold": 0},
        {"moisture_threshold": 101},
        {"water_requirement": 0},
        {"priority": 0},
        {"priority": 6},
        {"area": 0},
    ],
)
def test_field_validation(kwargs: dict[str, float]) -> None:
    base = {
        "field_id": "F",
        "area": 10,
        "crop": "x",
        "moisture_threshold": 35,
        "water_requirement": 10,
        "priority": 3,
    }
    base.update(kwargs)
    with pytest.raises(ValueError):
        Field(**base)  # type: ignore[arg-type]


def test_schedule_totals_and_validate() -> None:
    from datetime import datetime

    now = datetime(2026, 1, 1, 6)
    s = Schedule("x", 30, [ScheduleEntry(1, "A", 20, now, "r")])
    assert s.total_water == 20 and s.unused_water == 10
    s.validate()
    s.entries.append(ScheduleEntry(2, "B", 20, now, "r"))
    with pytest.raises(ValueError):
        s.validate()


def test_candidate_is_immutable() -> None:
    c = Candidate("A", 1, 1.0, 1.0, "r")
    with pytest.raises(AttributeError):
        c.water = 5  # type: ignore[misc]
