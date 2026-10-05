"""Integration tests for end-to-end scheduler execution and strategy swapping."""

import asyncio
from app.main import build_system
from app.scheduler.scheduler import DPScheduler, GreedyScheduler

FAST = (0.001, 0.002)


def test_end_to_end_irrigation_cycle() -> None:
    system = build_system(seed=42, budget=40, delay=FAST)
    result = asyncio.run(system.run_cycle(40))
    s = result.schedule
    assert s.total_water <= 40
    assert len(s.entries) > 0
    # verify strictly ordered timestamps
    starts = [e.start for e in s.entries]
    assert starts == sorted(starts)


def test_strategy_swap_maintains_invariants() -> None:
    system = build_system(seed=42, budget=50, delay=FAST)
    inputs = asyncio.run(system.collect_inputs())

    system.set_scheduler(GreedyScheduler())
    greedy_plan = system.plan(inputs, 50)

    system.set_scheduler(DPScheduler())
    dp_plan = system.plan(inputs, 50)

    assert greedy_plan.schedule.total_water <= 50
    assert dp_plan.schedule.total_water <= 50
    assert dp_plan.schedule.total_benefit >= greedy_plan.schedule.total_benefit - 1e-6
