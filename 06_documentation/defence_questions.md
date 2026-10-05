# Defence Q&A

**Problem?** Fixed-schedule irrigation wastes water. We schedule by soil moisture, rain forecast, field priority and a limited water budget.

**Why Greedy?** O(n log n) heuristic: highest benefit per litre first. Fast, near-optimal (0.2-0.3% gap in our benchmark) but not guaranteed optimal.

**Why DP?** The problem is 0/1 knapsack; DP gives the optimum for integer litres in O(nW). We verify it against brute force with Hypothesis.

**Why both?** To quantify the speed vs quality trade-off (see `docs/performance.md`).

**Why asyncio, not multiprocessing, for sensors?** Polling is I/O-bound; coroutines overlap waiting without extra processes. The GIL only constrains CPU-bound threads.

**Where do you use multiprocessing?** CPU-bound DP jobs in the benchmark (`ProcessPoolExecutor`).

**Which design pattern?** Strategy - `Scheduler` ABC with Greedy/DP implementations, swapped via `set_scheduler`.

**Pure function example?** `calculate_irrigation_need`, `weather_adjustment`, `calculate_benefit`.

**How do you know it's correct?** Unit + integration + e2e + property tests (DP matches brute force; budget never exceeded), 99% coverage, mypy strict, ruff, CI.

**What if a sensor fails?** `_safe_read` times out/logs and skips it; tested with `FailingSensor`.

**Limitations?** Simulated sensors/weather; one rain probability for all fields; benefit model is a heuristic; DP table is O(nW) memory.

**How did you use AI responsibly?** See `docs/ai_assisted_development.md`.
