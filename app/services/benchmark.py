"""Benchmarks: sequential vs async polling, Greedy vs DP, CPU-bound parallelism."""

from __future__ import annotations

import asyncio
import random
import time
import tracemalloc
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from app.algorithms.dynamic_programming import dynamic_schedule
from app.algorithms.greedy import greedy_schedule
from app.models.field import Field
from app.models.irrigation import Candidate
from app.sensors.manager import SensorManager
from app.sensors.simulator import build_simulated_sensors


@dataclass(frozen=True)
class PollingResult:
    sensors: int
    sequential: float
    concurrent: float

    @property
    def speedup(self) -> float:
        return self.sequential / self.concurrent if self.concurrent else float("inf")


@dataclass(frozen=True)
class SchedulerResult:
    fields: int
    budget: int
    greedy_time: float
    greedy_water: int
    greedy_benefit: float
    dp_time: float
    dp_water: int
    dp_benefit: float
    dp_peak_kib: float


def make_fields(n: int) -> list[Field]:
    return [Field(f"F{i:03d}", 1000, "Crop", 35, 30, 3) for i in range(n)]


def make_candidates(n: int, seed: int = 1) -> list[Candidate]:
    rng = random.Random(seed)
    return [
        Candidate(f"F{i:03d}", rng.randint(5, 60), rng.uniform(10, 200), 20.0, "Synthetic")
        for i in range(n)
    ]


async def _time_polling(n: int, delay: tuple[float, float]) -> PollingResult:
    manager = SensorManager(build_simulated_sensors(make_fields(n), delay_range=delay), timeout=10)
    t0 = time.perf_counter()
    await manager.collect_sequential()
    seq = time.perf_counter() - t0
    t0 = time.perf_counter()
    await manager.collect_readings()
    conc = time.perf_counter() - t0
    return PollingResult(n, seq, conc)


def benchmark_polling(
    sizes: tuple[int, ...] = (10, 25, 50, 100, 500),
    delay: tuple[float, float] = (0.002, 0.008),
) -> list[PollingResult]:
    return [asyncio.run(_time_polling(n, delay)) for n in sizes]


def _timed(fn, candidates: list[Candidate], budget: int):  # type: ignore[no-untyped-def]
    t0 = time.perf_counter()
    chosen = fn(candidates, budget)
    return chosen, time.perf_counter() - t0


def benchmark_schedulers(
    sizes: tuple[int, ...] = (10, 50, 100, 200), seed: int = 1
) -> list[SchedulerResult]:
    results: list[SchedulerResult] = []
    for n in sizes:
        cands = make_candidates(n, seed)
        budget = sum(c.water for c in cands) // 3
        g, gt = _timed(greedy_schedule, cands, budget)
        tracemalloc.start()
        d, dt = _timed(dynamic_schedule, cands, budget)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        results.append(
            SchedulerResult(
                n,
                budget,
                gt,
                sum(c.water for c in g),
                sum(c.benefit for c in g),
                dt,
                sum(c.water for c in d),
                sum(c.benefit for c in d),
                peak / 1024,
            )
        )
    return results


def _dp_job(args: tuple[int, int]) -> float:
    n, seed = args
    cands = make_candidates(n, seed)
    chosen = dynamic_schedule(cands, sum(c.water for c in cands) // 3)
    return sum(c.benefit for c in chosen)


def benchmark_multiprocessing(jobs: int = 8, n: int = 150, workers: int = 4) -> tuple[float, float]:
    """CPU-bound DP jobs: serial vs process pool (bypasses the GIL)."""
    args = [(n, s) for s in range(jobs)]
    t0 = time.perf_counter()
    serial = [_dp_job(a) for a in args]
    t_serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        parallel = list(pool.map(_dp_job, args))
    t_parallel = time.perf_counter() - t0
    assert serial == parallel
    return t_serial, t_parallel


def format_report(polling: list[PollingResult], sched: list[SchedulerResult]) -> str:
    lines = ["=" * 66, "SENSOR POLLING: sequential vs asyncio", "=" * 66]
    lines.append(f"{'Sensors':>8} {'Sequential(s)':>14} {'Async(s)':>10} {'Speedup':>9}")
    for p in polling:
        lines.append(
            f"{p.sensors:>8} {p.sequential:>14.4f} {p.concurrent:>10.4f} {p.speedup:>8.1f}x"
        )
    lines += ["", "=" * 66, "SCHEDULERS: Greedy vs Dynamic Programming", "=" * 66]
    for s in sched:
        gap = (s.dp_benefit - s.greedy_benefit) / s.dp_benefit * 100 if s.dp_benefit else 0
        lines.append(f"Fields={s.fields}  Budget={s.budget} L")
        lines.append(
            f"  Greedy : {s.greedy_time:.6f}s  water={s.greedy_water:>5}"
            f"  benefit={s.greedy_benefit:9.2f}"
        )
        lines.append(
            f"  DP     : {s.dp_time:.6f}s  water={s.dp_water:>5}"
            f"  benefit={s.dp_benefit:9.2f}  peak mem={s.dp_peak_kib:.0f} KiB"
        )
        lines.append(f"  Greedy benefit gap vs optimal: {gap:.2f}%")
    return "\n".join(lines)
