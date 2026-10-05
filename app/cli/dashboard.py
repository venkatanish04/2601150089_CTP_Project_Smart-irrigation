"""Interactive CLI dashboard and text renderers."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable

from app.models.irrigation import Candidate, Schedule
from app.models.sensor import SoilReading
from app.models.weather import WeatherForecast
from app.scheduler.scheduler import DPScheduler, GreedyScheduler
from app.services.benchmark import (
    benchmark_polling,
    benchmark_schedulers,
    format_report,
)
from app.services.irrigation import CycleResult, Inputs, IrrigationSystem
from app.services.monitoring import UrgentQueue

LINE = "-" * 52
BANNER = "=" * 52

MENU = f"""{BANNER}
        SMART IRRIGATION SYSTEM
{BANNER}

1. View sensor readings
2. View weather forecast
3. Calculate irrigation needs
4. Run Greedy scheduler
5. Run DP scheduler
6. Compare algorithms
7. Run sensor simulation (sequential vs async)
8. Run performance benchmark
9. Exit
"""


def render_readings(readings: dict[str, SoilReading]) -> str:
    rows = [
        f"{r.field_id}   Moisture: {r.moisture:>5.1f}%   Temperature: {r.temperature:.1f}°C"
        for r in sorted(readings.values(), key=lambda r: r.field_id)
    ]
    return "\n".join(["Sensor Readings", LINE, *rows])


def render_forecast(f: WeatherForecast) -> str:
    return "\n".join(
        [
            "Weather",
            LINE,
            f"Rain Probability: {f.rainfall_probability:.0f}%",
            f"Temperature: {f.temperature:.1f}°C",
            f"Expected Rainfall: {f.rainfall_mm:.1f} mm",
        ]
    )


def render_needs(candidates: list[Candidate]) -> str:
    if not candidates:
        return "No field needs irrigation."
    queue = UrgentQueue(candidates)  # heap gives urgency order
    by_id = {c.field_id: c for c in candidates}
    rows = [f"{'Field':<6}{'Moisture':>9}{'Water':>8}{'Benefit':>9}  Reason"]
    while len(queue):
        c = by_id[queue.pop()]
        rows.append(
            f"{c.field_id:<6}{c.moisture:>8.1f}%{c.water:>6} L{c.benefit:>9.1f}  {c.reason}"
        )
    return "\n".join(["Irrigation Needs (most urgent first)", LINE, *rows])


def render_schedule(s: Schedule) -> str:
    rows = [f"{'Priority':<10}{'Start':<7}{'Field':<7}{'Water':<8}Reason"]
    rows += [
        f"{e.order:<10}{e.start:%H:%M}  {e.field_id:<7}{e.water:<4}L   {e.reason}"
        for e in s.entries
    ]
    return "\n".join(
        [
            f"IRRIGATION PLAN ({s.algorithm})",
            LINE,
            *rows,
            "",
            f"Total Water : {s.total_water} L / {s.budget} L budget",
            f"Unused Water: {s.unused_water} L",
            f"Benefit     : {s.total_benefit:.1f}",
            f"Compute Time: {s.elapsed:.6f} s",
        ]
    )


def render_comparison(greedy: Schedule, dp: Schedule) -> str:
    out = [BANNER, "ALGORITHM COMPARISON", BANNER, ""]
    for s in (greedy, dp):
        out += [
            s.algorithm,
            LINE,
            f"Execution Time     : {s.elapsed:.6f} sec",
            f"Water Used         : {s.total_water} L",
            f"Irrigation Benefit : {s.total_benefit:.1f}",
            f"Fields             : {[e.field_id for e in s.entries]}",
            "",
        ]
    return "\n".join(out)


class Dashboard:
    def __init__(
        self,
        system: IrrigationSystem,
        budget: int,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        self.system = system
        self.budget = budget
        self._in = input_fn
        self._out = output_fn
        self._inputs: Inputs | None = None

    def _refresh(self) -> Inputs:
        self._inputs = asyncio.run(self.system.collect_inputs())
        return self._inputs

    def _current(self) -> Inputs:
        return self._inputs or self._refresh()

    def _plan(self, which: str) -> CycleResult:
        scheduler = GreedyScheduler() if which == "greedy" else DPScheduler()
        return self.system.plan(self._current(), self.budget, scheduler)

    def _sensor_simulation(self) -> str:
        mgr = self.system.sensor_manager

        async def run() -> tuple[float, float]:
            t0 = time.perf_counter()
            await mgr.collect_sequential()
            t1 = time.perf_counter()
            await mgr.collect_readings()
            return t1 - t0, time.perf_counter() - t1

        seq, conc = asyncio.run(run())
        return (
            f"Sensors: {len(mgr.sensors)}\n"
            f"Sequential polling: {seq:.3f} s\n"
            f"Async polling     : {conc:.3f} s\n"
            f"Speedup           : {seq / conc:.1f}x"
        )

    def handle(self, choice: str) -> bool:
        """Run one menu choice. Returns False when the user exits."""
        out = self._out
        if choice == "1":
            out(render_readings(self._refresh().readings))
        elif choice == "2":
            out(render_forecast(self._current().forecast))
        elif choice == "3":
            result = self._plan("greedy")
            out(render_needs(result.candidates))
        elif choice == "4":
            out(render_schedule(self._plan("greedy").schedule))
        elif choice == "5":
            out(render_schedule(self._plan("dp").schedule))
        elif choice == "6":
            g, d = self._plan("greedy"), self._plan("dp")
            out(render_comparison(g.schedule, d.schedule))
        elif choice == "7":
            out(self._sensor_simulation())
        elif choice == "8":
            out("Running benchmark (takes a few seconds)...")
            out(
                format_report(benchmark_polling((10, 50, 100)), benchmark_schedulers((10, 50, 100)))
            )
        elif choice == "9":
            out("Goodbye.")
            return False
        else:
            out("Invalid choice, enter 1-9.")
        return True

    def run(self) -> None:
        running = True
        while running:
            self._out(MENU)
            running = self.handle(self._in("Enter choice: ").strip())
            self._out("")
