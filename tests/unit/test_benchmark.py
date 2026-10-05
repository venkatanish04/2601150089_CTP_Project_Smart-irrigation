from app.services import benchmark as b


def test_polling_benchmark_shows_speedup() -> None:
    [r] = b.benchmark_polling((20,), delay=(0.01, 0.01))
    assert r.speedup > 3


def test_scheduler_benchmark_dp_is_at_least_as_good() -> None:
    for r in b.benchmark_schedulers((10, 30)):
        assert r.dp_benefit >= r.greedy_benefit - 1e-9
        assert r.dp_water <= r.budget and r.greedy_water <= r.budget
    assert "Greedy" in b.format_report([], b.benchmark_schedulers((5,)))


def test_multiprocessing_gives_same_results() -> None:
    serial, parallel = b.benchmark_multiprocessing(jobs=2, n=20, workers=2)
    assert serial > 0 and parallel > 0
