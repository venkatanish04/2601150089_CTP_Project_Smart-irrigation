"""Run: python -m benchmarks.scheduler_benchmark"""

from app.services.benchmark import (
    benchmark_multiprocessing,
    benchmark_polling,
    benchmark_schedulers,
    format_report,
)

if __name__ == "__main__":
    print(format_report(benchmark_polling(), benchmark_schedulers()))
    serial, parallel = benchmark_multiprocessing()
    print(f"\nCPU-bound DP: serial {serial:.3f}s | multiprocessing {parallel:.3f}s")
