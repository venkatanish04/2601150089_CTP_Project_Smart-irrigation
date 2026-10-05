# Concurrency

* **I/O-bound** (sensor and weather waits): `asyncio.gather` - while one sensor "waits", others progress. Single thread, so the GIL is irrelevant.
* **CPU-bound** (large DP tables): threads would not help because of the GIL; `ProcessPoolExecutor` runs jobs in separate processes (`benchmark_multiprocessing`).
* Resilience: each read is wrapped in `asyncio.wait_for` with a timeout; failures are logged and the field is skipped for that cycle.

Note: the sandbox used to develop this had **1 CPU core**, so multiprocessing showed no speedup (~1.0x). On a multi-core machine the CPU-bound jobs scale with core count; run `python -m app.main --benchmark` on your own machine to get real numbers for your defence.
