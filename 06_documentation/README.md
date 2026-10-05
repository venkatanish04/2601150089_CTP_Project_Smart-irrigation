# Smart Irrigation Scheduling System

Sensor-driven irrigation scheduler using **Greedy** and **Dynamic Programming** (0/1 knapsack),
**asyncio** sensor polling, and a **Strategy-pattern** OOP design. Pure Python 3.12, no runtime dependencies.

## Quick start
```bash
pip install -e ".[dev]"          # dev tools only; the app itself needs nothing
python -m app.main               # interactive CLI dashboard
python -m app.main --demo        # one-shot demo (Greedy vs DP)
python -m app.main --demo --budget 30 --log schedule.log
python -m app.main --benchmark   # sequential vs async, Greedy vs DP, multiprocessing
```

## Quality gates
```bash
ruff check . && black --check . && mypy app/
pytest --cov=app --cov-report=term-missing
```
Current status: 60 tests passing, 99% coverage, mypy `--strict` clean, ruff clean.

## Docker
```bash
docker build -t smart-irrigation .
docker run --rm -it smart-irrigation
docker run --rm smart-irrigation python -m app.main --demo
```

## How it works
1. `SimulatedSensor`s are polled concurrently with `asyncio.gather` (`SensorManager`); a failed or slow sensor is skipped, not fatal.
2. `SimulatedWeatherService` gives rain probability; fetched concurrently with sensors.
3. Pure functions compute need = `requirement x deficit/threshold`, reduced by rain probability, rounded up to whole litres.
4. Each field needing water becomes a `Candidate(water, benefit)`; benefit = `deficit ratio x priority x 100 x (1 - rain)`.
5. A `Scheduler` strategy (`GreedyScheduler` or `DPScheduler`) picks fields within the water budget.
6. `build_schedule` orders fields by benefit, assigns 20-minute slots from 06:00 and validates the budget.

## Layout
See `docs/architecture.md`. Defence material: `docs/defence_questions.md`, `docs/requirements_mapping.md`.
