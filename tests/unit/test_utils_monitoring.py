import logging

import pytest

from app.models.irrigation import Candidate, Schedule
from app.services.monitoring import UrgentQueue, active_fields, moisture_map
from app.utils.functional import filter_fields
from app.utils.logger import ScheduleLogger, setup_logging
from app.utils.timing import TIMINGS, measure_time


def test_measure_time_records_and_preserves_result() -> None:
    @measure_time
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    assert len(TIMINGS["add"]) == 1 and add.__name__ == "add"


def test_filter_fields_higher_order() -> None:
    assert filter_fields(range(10), lambda x: x % 2 == 0) == [0, 2, 4, 6, 8]


def test_urgent_queue_pops_highest_benefit_first(candidates: list[Candidate]) -> None:
    q = UrgentQueue(candidates)
    assert len(q) == 4
    assert q.pop() == "B"  # benefit 40 is highest
    assert q.pop() == "C"


def test_set_and_dict_helpers(candidates: list[Candidate]) -> None:
    assert active_fields(candidates) == {"A", "B", "C", "D"}
    assert moisture_map(candidates)["A"] == 20.0


def test_schedule_logger_writes_and_closes(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "s.log"
    with ScheduleLogger(str(path)) as log:
        log.write(Schedule("Greedy", 10))
    assert "Greedy" in path.read_text()
    with pytest.raises(RuntimeError):
        log.write(Schedule("x", 1))  # closed


def test_schedule_logger_closes_on_error(tmp_path) -> None:  # type: ignore[no-untyped-def]
    logger = ScheduleLogger(str(tmp_path / "e.log"))
    with pytest.raises(ValueError), logger:
        raise ValueError("boom")
    assert logger._file is None


def test_setup_logging() -> None:
    setup_logging(logging.INFO)
