# Live Demonstration & Defence Walkthrough Script

Use this step-by-step walkthrough script during your live project defence and evaluation.

---

## 1. Opening Statement (30 seconds)
> *"Good morning / afternoon evaluators. Today I present the **Smart Irrigation Scheduling System**, an intelligent sensor-driven platform designed to eliminate agricultural water wastage. Rather than relying on rigid, fixed-timer irrigation (which waters regardless of soil moisture or rain), our system dynamically collects sensor telemetry across field zones, factors in localized precipitation forecasts, and formulates an optimal irrigation schedule subject to strict water budget constraints using Greedy heuristics and Dynamic Programming."*

---

## 2. Command-Line Demo Actions

### Action A: Instant Automated One-Shot Demo
Run in terminal:
```powershell
python -m app.main --demo --budget 40 --log schedule.log
```
**Talking Points to Show the Evaluators:**
1. **Telemetry & Weather**: Show field sensor readings ($F01$ through $F05$) and rain forecast ($10\%$).
2. **Deficit Calculation**: Notice $F02$ has moisture $42.6\% \ge 35\%$ threshold, so its water need is $0$ L (skipped!).
3. **Budget Constraint**: Budget is $40$ L. Candidates need $49$ L total.
4. **Greedy Schedule**: Selects highest benefit-per-litre ($F05$ then $F01$), consuming $36$ L with $4$ L unused.
5. **DP Schedule**: Knapsack optimization achieves the exact optimal allocation.
6. **Logging**: Show `schedule.log` to prove persistent execution logging via Python Context Manager.

---

### Action B: Interactive Dashboard Walkthrough
Run in terminal:
```powershell
python -m app.main
```
Demonstrate the menu options:
- **Option 1**: Display live soil moisture and temperature readings.
- **Option 2**: Display real-time weather forecast.
- **Option 3**: Display calculated irrigation needs ranked by priority using Python's `heapq`.
- **Option 4 & 5**: Run Greedy and DP schedulers interactively.
- **Option 6**: Side-by-side comparison table proving execution time, water utilization, and total irrigation benefit.
- **Option 7**: Concurrency demonstration: Sequential vs Asyncio polling.

---

### Action C: Concurrency & Performance Benchmarks
Run in terminal:
```powershell
python -m app.main --benchmark
```
**Key Benchmark Metrics to Highlight:**
1. **Sensor Polling Scalability**:
   - $10$ sensors: $0.16$s sequential vs $0.015$s async ($10.9\times$ speedup)
   - $100$ sensors: $1.53$s sequential vs $0.011$s async ($139.2\times$ speedup)
   - $500$ sensors: $7.47$s sequential vs $0.021$s async ($349.8\times$ speedup)
   *Explanation*: Sensor polling is I/O-bound. Asyncio coroutines interleave I/O latency without GIL contention.
2. **Algorithm Trade-off (Greedy vs DP)**:
   - Greedy runs in $O(n \log n)$ time ($\sim 50\,\mu\text{s}$ even for 200 fields).
   - DP guarantees mathematical optimality ($O(nW)$ pseudo-polynomial) at the expense of higher CPU time ($2.1$s) and memory ($8.6$ MB).
3. **Multiprocessing**:
   - For CPU-bound batch DP optimizations, Python's `ProcessPoolExecutor` bypasses the GIL across multiple OS processes ($1.5\times$ speedup).

---

### Action D: Automated Quality & Testing Suite
Run in terminal:
```powershell
pytest --cov=app --cov-report=term-missing
```
Highlight:
- **60 Automated Tests**: Unit, Integration, E2E, and Property-based.
- **99% Test Coverage**: Thorough test coverage across all application modules.
- **Property-Based Testing (Hypothesis)**: Formally verifies invariants (e.g., allocated water $\le$ budget, zero duplicates, and DP matching brute-force combinatorial search).

Run static analysis:
```powershell
mypy app tests
ruff check .
black --check app tests benchmarks
```
Highlight:
- Zero type errors under `mypy --strict`.
- Zero lint violations with Ruff.
- PEP 8 compliance verified by Black.

---

## 3. High-Yield Viva / Defence Questions & Answers

### Q1: Why model irrigation scheduling as a 0/1 Knapsack problem?
> *"Each field zone is a discrete unit that either receives its required irrigation depth in the current cycle or does not (0/1 decision). Each field has a water requirement (weight $w_i$) and an urgency benefit score (value $v_i$). Given a finite water reservoir (capacity $W$), our objective is $\max \sum v_i x_i$ subject to $\sum w_i x_i \le W$, which maps directly to the NP-hard 0/1 Knapsack problem."*

### Q2: Why did you implement both Greedy and Dynamic Programming?
> *"To demonstrate algorithmic trade-offs. The Greedy heuristic sorts by density ($v_i / w_i$) in $O(n \log n)$ time and $O(n)$ space, producing solutions within $<0.3\%$ of optimal in microseconds. The Dynamic Programming approach guarantees the true global optimum for integer capacities in $O(nW)$ time and space. Comparing both allows us to evaluate execution latency versus optimality gap."*

### Q3: When does the Greedy algorithm fail to achieve the optimal solution?
> *"Greedy can leave unused budget capacity because it greedily picks smaller density items. In our test suite (`test_dp_beats_greedy_on_classic_case`), items with (10L, 60), (20L, 100), (30L, 120) with budget 50L cause Greedy to pick (10L + 20L) = benefit 160. Dynamic Programming picks (20L + 30L) = benefit 220, achieving 37.5% higher benefit."*

### Q4: Why use asyncio instead of multiprocessing for sensor communication?
> *"Sensor telemetry collection is I/O-bound: the CPU spends most of its time waiting for network packets or sensor hardware responses. Coroutines in `asyncio` cooperatively multitask during sleep/wait periods in a single thread with minimal overhead. Multiprocessing would introduce unnecessary process creation and IPC serialization overhead. We reserved multiprocessing specifically for CPU-bound batch DP computation."*

### Q5: How did you apply Object-Oriented Design principles?
> *"We utilized the **Strategy Pattern** via an abstract base class `Scheduler` with concrete implementations `GreedyScheduler` and `DPScheduler`. The `IrrigationSystem` interacts only with the abstract interface, allowing runtime strategy switching without modifying client code (Open-Closed Principle). Furthermore, we favored composition over inheritance: `IrrigationSystem` is composed of a `SensorManager`, `WeatherService`, and `Scheduler`."*

### Q6: Give examples of Functional Programming in your codebase.
> *"All core mathematical routines in `app/algorithms/scoring.py` (`calculate_irrigation_need`, `weather_adjustment`, `calculate_benefit`) are **pure functions** that produce deterministic outputs solely from inputs without mutating state. We also use higher-order functions (`filter_fields`, custom lambdas for sorting), iterators, and generators."*
