# Software Requirements Specification (SRS)

## 1. Functional Requirements (FR)

| Requirement ID | Description | Source Module | Verification Test |
|---|---|---|---|
| **FR-01** | The system shall asynchronously poll in-situ soil moisture, temperature, and humidity sensors across all configured fields without blocking the main event loop. | `app/sensors/` | `tests/unit/test_sensors_weather.py`, `tests/property/` |
| **FR-02** | The system shall acquire weather forecast data, including probability of precipitation and expected rainfall in mm. | `app/weather/` | `tests/unit/test_sensors_weather.py` |
| **FR-03** | The system shall calculate the net irrigation need based on soil moisture deficit and discount water volume proportionally according to forecasted rainfall. | `app/algorithms/scoring.py` | `tests/unit/test_scoring.py` |
| **FR-04** | The system shall assign an urgency benefit score to each candidate plot combining deficit percentage, crop economic priority, and rainfall factor. | `app/algorithms/scoring.py` | `tests/unit/test_scoring.py` |
| **FR-05** | The system shall ensure total scheduled water never exceeds the total reservoir capacity budget ($W$). | `app/services/irrigation.py` | `tests/property/test_properties.py` |
| **FR-06** | The system shall provide a fast Greedy scheduling strategy operating in $\mathcal{O}(n \log n)$ time by prioritizing candidates by benefit density. | `app/algorithms/greedy.py` | `tests/unit/test_algorithms.py` |
| **FR-07** | The system shall provide an optimal Dynamic Programming 0/1 knapsack scheduling strategy operating in $\mathcal{O}(nW)$ pseudo-polynomial time. | `app/algorithms/dynamic_programming.py` | `tests/property/test_properties.py` |
| **FR-08** | The system shall formulate a serialized chronological dispatch plan assigning sequential time slots to selected plots. | `app/services/irrigation.py` | `tests/integration/test_pipeline.py` |
| **FR-09** | The system shall provide an interactive CLI dashboard allowing the user to view readings, forecasts, candidate needs, and side-by-side algorithm benchmarks. | `app/cli/dashboard.py` | `tests/e2e/test_cli.py` |

---

## 2. Non-Functional Requirements (NFR)

| Requirement ID | Category | Target Metric |
|---|---|---|
| **NFR-01** | Fault Tolerance | Unresponsive or timing-out field sensors must be safely isolated; one sensor failure must never crash the decision cycle. |
| **NFR-02** | Latency & Scalability | Concurrent sensor polling across 100+ simulated nodes must complete in under 50 ms. |
| **NFR-03** | Type Safety | Codebase must maintain 100% type annotations passing `mypy --strict` with zero errors. |
| **NFR-04** | Code Quality | Codebase must comply with PEP 8 standards, zero lint warnings via `ruff`, and formatted via `black`. |
| **NFR-05** | Test Coverage | Automated test suite must maintain $\ge 90\%$ statement coverage via `pytest-cov`. |
| **NFR-06** | Portability | System must execute seamlessly in containerized environments (Docker, docker-compose). |
