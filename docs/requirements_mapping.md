# Mapping to the defence PDF

| Responsibility | Implementation |
|---|---|
| Decomposition / abstraction | sensors -> weather -> scoring -> scheduler; ABCs and dataclasses |
| Pattern recognition | resource allocation = 0/1 knapsack |
| Greedy / DP + complexity | `algorithms/`, `docs/algorithms.md` |
| Data structures | list, dict, set, heapq, DP table |
| Iterators / generators / comprehensions | `sensors/manager.py`, `services/`, `utils/` |
| Decorators / context managers | `measure_time`, `ScheduleLogger` |
| OOP, inheritance, composition, Strategy | `scheduler/`, `services/irrigation.py` |
| Type hints / pure / higher-order functions | `mypy --strict`, `scoring.py`, `filter_fields` |
| asyncio / multiprocessing / GIL | `sensors/manager.py`, `services/benchmark.py`, `docs/concurrency.md` |
| pytest / Hypothesis / coverage | `tests/` |
| mypy / ruff / black | `pyproject.toml`, CI |
| CI/CD + Docker | `.github/workflows/ci.yml`, `Dockerfile` |
| Performance evaluation | `python -m app.main --benchmark`, `docs/performance.md` |
| Live demo | `python -m app.main` / `--demo` |
