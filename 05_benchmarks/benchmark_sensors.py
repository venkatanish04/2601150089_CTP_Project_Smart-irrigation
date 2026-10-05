"""Benchmark comparison between Sequential and Asyncio sensor polling."""

from __future__ import annotations

import json
from pathlib import Path
from app.services.benchmark import benchmark_polling

RESULTS_DIR = Path(__file__).parent / "benchmark_results"


def run_sensor_benchmarks() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    print("Executing Sensor Polling Benchmarks (Sequential vs asyncio)...")
    results = benchmark_polling()

    data = [
        {
            "sensors": r.sensors,
            "sequential_s": r.sequential,
            "concurrent_s": r.concurrent,
            "speedup": round(r.speedup, 1),
        }
        for r in results
    ]
    json_path = RESULTS_DIR / "sensor_benchmark.json"
    json_path.write_text(json.dumps(data, indent=2))
    print(f"Sensor polling benchmark results written to: {json_path}")


if __name__ == "__main__":
    run_sensor_benchmarks()
