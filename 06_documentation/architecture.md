# Architecture

```
SensorManager (asyncio) ─┐
                         ├─> IrrigationSystem.collect_inputs ─> build_candidates (pure functions)
WeatherService (async) ──┘                                              │
                                                                         ▼
                        Scheduler (Strategy) ◄────────────── IrrigationSystem.plan
                        ├─ GreedyScheduler                              │
                        └─ DPScheduler                                  ▼
                                                              Schedule (validated) ─> CLI Dashboard
```

* **Abstraction**: `Sensor`, `WeatherService`, `Scheduler` are ABCs.
* **Inheritance / polymorphism**: `GreedyScheduler`, `DPScheduler` implement `Scheduler`; `SimulatedSensor`/`FailingSensor` implement `Sensor`.
* **Composition**: `IrrigationSystem` holds a `SensorManager`, `WeatherService` and `Scheduler`.
* **Strategy pattern**: `IrrigationSystem.set_scheduler()` swaps algorithms at runtime.
* **Immutability**: models are frozen dataclasses; scoring functions are pure.

## Python feature map
| Feature | Where |
|---|---|
| list / dict / set / heap | candidates; readings dict; `active_fields`; `UrgentQueue` (heapq) |
| iterator | `SensorReadingIterator` |
| generators | `critical_readings`, async generator `SensorManager.stream` |
| comprehensions | `build_schedule`, `filter_fields`, `moisture_map` |
| decorator | `utils/timing.measure_time` (ParamSpec-typed) |
| context manager | `utils/logger.ScheduleLogger` |
| higher-order fn | `utils/functional.filter_fields` |
| type hints | everywhere, `mypy --strict` |
