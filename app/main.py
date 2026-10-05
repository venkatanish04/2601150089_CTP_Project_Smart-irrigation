"""Entry point: ``python -m app.main [--demo | --compare | --benchmark]``."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from app.cli.dashboard import (
    Dashboard,
    render_comparison,
    render_forecast,
    render_needs,
    render_readings,
    render_schedule,
)
from app.scheduler.scheduler import DPScheduler, GreedyScheduler
from app.sensors.manager import SensorManager
from app.sensors.simulator import build_simulated_sensors
from app.services.benchmark import (
    benchmark_multiprocessing,
    benchmark_polling,
    benchmark_schedulers,
    format_report,
)
from app.services.irrigation import IrrigationSystem
from app.utils.config import DEFAULT_FIELDS, DEMO_MOISTURE, Settings
from app.utils.logger import ScheduleLogger, setup_logging
from app.weather.service import SimulatedWeatherService


def build_system(
    seed: int = 42, budget: int = 40, delay: tuple[float, float] = (0.1, 0.5)
) -> IrrigationSystem:
    settings = Settings(water_budget=budget)
    sensors = build_simulated_sensors(
        DEFAULT_FIELDS, profile=DEMO_MOISTURE, seed=seed, delay_range=delay
    )
    return IrrigationSystem(
        DEFAULT_FIELDS,
        SensorManager(sensors, timeout=settings.sensor_timeout),
        SimulatedWeatherService(settings.demo_rain_probability, seed=seed),
        GreedyScheduler(),
        settings,
    )


def run_demo(system: IrrigationSystem, budget: int, log_path: str | None = None) -> None:
    inputs = asyncio.run(system.collect_inputs())
    print(render_readings(inputs.readings), "\n")
    print(render_forecast(inputs.forecast), "\n")
    greedy = system.plan(inputs, budget, GreedyScheduler())
    dp = system.plan(inputs, budget, DPScheduler())
    print(render_needs(greedy.candidates), "\n")
    print(render_schedule(greedy.schedule), "\n")
    print(render_schedule(dp.schedule), "\n")
    print(render_comparison(greedy.schedule, dp.schedule))
    if log_path:
        with ScheduleLogger(log_path) as log:
            log.write(greedy.schedule)
            log.write(dp.schedule)
    print("Schedule generated successfully.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smart Irrigation Scheduler")
    parser.add_argument("--demo", action="store_true", help="one-shot demo run")
    parser.add_argument("--benchmark", action="store_true", help="run benchmarks")
    parser.add_argument("--budget", type=int, default=40, help="water budget (L)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--log", default=None, help="append schedules to this file")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    setup_logging(logging.DEBUG if args.verbose else logging.WARNING)

    if args.benchmark:
        print(format_report(benchmark_polling(), benchmark_schedulers()))
        t_serial, t_par = benchmark_multiprocessing()
        print(
            f"\nCPU-bound DP jobs: serial {t_serial:.3f}s vs "
            f"multiprocessing {t_par:.3f}s ({t_serial / t_par:.1f}x)"
        )
        return 0

    system = build_system(args.seed, args.budget)
    if args.demo:
        run_demo(system, args.budget, args.log)
    else:
        Dashboard(system, args.budget).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
