"""IrrigationSystem: composes sensors + weather + a pluggable scheduler."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from datetime import time as dtime

from app.algorithms.scoring import build_candidates
from app.models.field import Field
from app.models.irrigation import Candidate, Schedule, ScheduleEntry
from app.models.sensor import SoilReading
from app.models.weather import WeatherForecast
from app.scheduler.scheduler import Scheduler
from app.sensors.manager import SensorManager
from app.utils.config import Settings
from app.weather.service import WeatherService


@dataclass
class Inputs:
    readings: dict[str, SoilReading]
    forecast: WeatherForecast


@dataclass
class CycleResult:
    readings: dict[str, SoilReading]
    forecast: WeatherForecast
    candidates: list[Candidate]
    schedule: Schedule


def build_schedule(
    chosen: list[Candidate],
    budget: int,
    algorithm: str,
    elapsed: float,
    settings: Settings | None = None,
    start: datetime | None = None,
) -> Schedule:
    """Order chosen fields by benefit and assign consecutive time slots."""
    cfg = settings or Settings()
    first = start or datetime.combine(date.today(), dtime(cfg.start_hour, 0))
    ordered = sorted(chosen, key=lambda c: c.benefit, reverse=True)
    entries = [
        ScheduleEntry(
            order=i + 1,
            field_id=c.field_id,
            water=c.water,
            start=first + timedelta(minutes=cfg.slot_minutes * i),
            reason=c.reason,
        )
        for i, c in enumerate(ordered)
    ]
    schedule = Schedule(
        algorithm=algorithm,
        budget=budget,
        entries=entries,
        total_benefit=sum(c.benefit for c in chosen),
        elapsed=elapsed,
    )
    schedule.validate()
    return schedule


class IrrigationSystem:
    def __init__(
        self,
        fields: list[Field],
        sensor_manager: SensorManager,
        weather_service: WeatherService,
        scheduler: Scheduler,
        settings: Settings | None = None,
    ) -> None:
        self.fields = fields
        self.sensor_manager = sensor_manager
        self.weather_service = weather_service
        self.scheduler = scheduler
        self.settings = settings or Settings()

    def set_scheduler(self, scheduler: Scheduler) -> None:
        """Swap the strategy at runtime."""
        self.scheduler = scheduler

    async def collect_inputs(self) -> Inputs:
        """Poll sensors and weather concurrently."""
        readings, forecast = await asyncio.gather(
            self.sensor_manager.collect_readings(),
            self.weather_service.get_forecast(),
        )
        return Inputs(readings, forecast)

    def plan(self, inputs: Inputs, budget: int, scheduler: Scheduler | None = None) -> CycleResult:
        strategy = scheduler or self.scheduler
        candidates = build_candidates(self.fields, inputs.readings, inputs.forecast)
        start = time.perf_counter()
        chosen = strategy.generate_schedule(candidates, budget)
        elapsed = time.perf_counter() - start
        schedule = build_schedule(chosen, budget, strategy.name, elapsed, self.settings)
        return CycleResult(inputs.readings, inputs.forecast, candidates, schedule)

    async def run_cycle(self, budget: int | None = None) -> CycleResult:
        inputs = await self.collect_inputs()
        return self.plan(inputs, budget if budget is not None else self.settings.water_budget)
