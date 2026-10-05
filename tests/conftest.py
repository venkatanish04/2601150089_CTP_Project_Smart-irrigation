import pytest

from app.models.irrigation import Candidate


@pytest.fixture
def candidates() -> list[Candidate]:
    # Classic case where greedy-by-ratio is suboptimal for budget 50:
    # ratios: A=1.2, B=1.0, C=1.0 -> greedy picks A(10) then B(40) ... see tests
    return [
        Candidate("A", 10, 12.0, 20.0, "r"),
        Candidate("B", 40, 40.0, 20.0, "r"),
        Candidate("C", 30, 30.0, 20.0, "r"),
        Candidate("D", 25, 24.0, 20.0, "r"),
    ]
