# Functional Programming & Concurrency

## 1. Pure Mathematical Functions
The system cleanly separates computational algorithms from stateful execution. The following functions in `app/algorithms/scoring.py` are strictly **pure**:
- `calculate_irrigation_need(moisture, threshold, water_requirement)`
- `weather_adjustment(water_required, rain_probability)`
- `calculate_priority(moisture, threshold, priority)`
- `calculate_benefit(moisture, threshold, priority, rain_probability)`

### Properties of Pure Functions:
1. **Referential Transparency**: Every call with identical arguments evaluates to identical results.
2. **Zero Side-Effects**: No global variables are modified; no I/O is performed.
3. **Trivial Testability**: Unit tests do not require mocks or setup fixtures.

## 2. Higher-Order Functions
- `filter_fields(fields, predicate)` in `app/utils/functional.py`: Takes a function as a parameter to filter field sequences.
- `sorted(candidates, key=lambda c: c.benefit / c.water, reverse=True)`: Higher-order density projection.

## 3. Concurrency & Python GIL Architecture
- **I/O-Bound**: Polling 100 sensors sequentially blocks on network latency. Using `asyncio.gather` overlaps waiting periods in a single OS thread. The GIL is released during socket/sleep I/O, yielding massive speedups (up to 349x).
- **CPU-Bound**: Tabulating large dynamic programming matrices blocks CPU cores. The GIL prevents multithreading from scaling across multiple cores. Therefore, `benchmark_multiprocessing()` uses `ProcessPoolExecutor` to spawn multiple OS processes with separate GIL instances.
