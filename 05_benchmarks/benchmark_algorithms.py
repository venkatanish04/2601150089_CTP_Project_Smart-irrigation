"""Benchmark comparison between Greedy and Dynamic Programming schedulers."""

from __future__ import annotations

import json
from pathlib import Path
from app.services.benchmark import benchmark_schedulers, format_report

RESULTS_DIR = Path(__file__).parent / "benchmark_results"


def run_algorithm_benchmarks() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    print("Executing Greedy vs Dynamic Programming Benchmarks...")
    results = benchmark_schedulers()

    # Save raw JSON results
    data = [
        {
            "fields": r.fields,
            "budget": r.budget,
            "greedy_time_s": r.greedy_time,
            "greedy_water_L": r.greedy_water,
            "greedy_benefit": r.greedy_benefit,
            "dp_time_s": r.dp_time,
            "dp_water_L": r.dp_water,
            "dp_benefit": r.dp_benefit,
            "dp_peak_kib": r.dp_peak_kib,
        }
        for r in results
    ]
    json_path = RESULTS_DIR / "algorithm_benchmark.json"
    json_path.write_text(json.dumps(data, indent=2))
    print(f"Algorithm benchmark results written to: {json_path}")


if __name__ == "__main__":
    run_algorithm_benchmarks()
