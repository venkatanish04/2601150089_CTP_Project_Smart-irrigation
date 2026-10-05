# AI Prompting Engineering & Specification Log

## Prompting Strategy: Specification-First & Constrained Prompts
Rather than broad, open-ended queries (e.g., *"write me an irrigation scheduler"*), prompts were engineered with strict constraints, clear interfaces, and explicit validation criteria.

### Prompt 1: Pure Scoring Functions
> *"Design a Python module `scoring.py` for calculating field irrigation requirements. All functions must be pure functions with zero side-effects and no global state. Include type hints for all arguments and return values using Python 3.12 syntax. If soil moisture is at or above the threshold, return 0.0. Discount the requirement proportionally by the rain probability (0 to 100%). Raise ValueError on negative moisture, non-positive threshold, or out-of-range rain probability. Do not import external third-party packages."*

### Prompt 2: 0/1 Knapsack Dynamic Programming
> *"Implement a 0/1 knapsack dynamic programming algorithm in Python to select an optimal subset of fields within a water budget $W$. Water requirements must be positive integers; benefits are positive floats. Time complexity must be $\mathcal{O}(nW)$ and space complexity $\mathcal{O}(nW)$. Return the reconstructed list of selected candidate objects, preserving their original order. Decorate the function with a timing decorator. Include type hints passing `mypy --strict`."*

### Prompt 3: Async Sensor Concurrency & Fault Tolerance
> *"Implement a `SensorManager` class that polls a list of `Sensor` objects concurrently using `asyncio.gather`. Each read must be wrapped in `asyncio.wait_for` with a configurable timeout. If any individual sensor times out or raises an exception, log a warning and omit that sensor from the result dictionary; do not allow a single sensor failure to terminate the polling cycle."*
