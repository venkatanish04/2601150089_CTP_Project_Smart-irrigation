"""Sensors -> readings -> needs -> weather -> scheduler -> schedule."""

import asyncio

from app.main import build_system
from app.scheduler.scheduler import DPScheduler, GreedyScheduler

FAST = (0.001, 0.003)


def test_full_pipeline_respects_budget_and_priorities() -> None:
    system = build_system(seed=1, budget=40, delay=FAST)
    result = asyncio.run(system.run_cycle(40))
    s = result.schedule
    assert s.total_water <= 40
    ids = [e.field_id for e in s.entries]
    assert "F02" not in ids  # moist field never irrigated
    assert ids[0] == "F05"  # critical field first
    starts = [e.start for e in s.entries]
    assert starts == sorted(starts)


def test_strategy_swap_at_runtime() -> None:
    system = build_system(seed=1, delay=FAST)
    inputs = asyncio.run(system.collect_inputs())
    system.set_scheduler(GreedyScheduler())
    g = system.plan(inputs, 40)
    system.set_scheduler(DPScheduler())
    d = system.plan(inputs, 40)
    assert (g.schedule.algorithm, d.schedule.algorithm) == ("Greedy", "Dynamic Programming")
    assert d.schedule.total_benefit >= g.schedule.total_benefit - 1e-9


def test_heavy_rain_means_no_irrigation() -> None:
    system = build_system(seed=1, delay=FAST)
    system.weather_service.rain_probability = 100  # type: ignore[attr-defined]
    result = asyncio.run(system.run_cycle(100))
    assert result.schedule.entries == []


def test_default_budget_is_used() -> None:
    system = build_system(seed=1, delay=FAST)
    assert asyncio.run(system.run_cycle()).schedule.budget == system.settings.water_budget
