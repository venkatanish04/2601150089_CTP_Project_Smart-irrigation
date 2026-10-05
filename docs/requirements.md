# Functional requirements (specification-first)

| ID | Requirement | Implemented in | Verified by |
|----|-------------|----------------|-------------|
| FR-01 | Collect soil-moisture readings | `sensors/` | `test_sensors_weather.py` |
| FR-02 | Obtain weather forecast | `weather/service.py` | `test_sensors_weather.py` |
| FR-03 | Calculate irrigation requirements | `algorithms/scoring.py` | `test_scoring.py`, property tests |
| FR-04 | Never exceed available water | `Schedule.validate`, both algorithms | `test_properties.py` |
| FR-05 | Generate an irrigation schedule | `services/irrigation.py` | `test_pipeline.py` |
| FR-06 | Greedy scheduling | `algorithms/greedy.py` | `test_algorithms.py` |
| FR-07 | Dynamic-programming scheduling | `algorithms/dynamic_programming.py` | brute-force property test |
| FR-08 | Poll sensors asynchronously | `sensors/manager.py` | speed test in `test_sensors_weather.py` |
| NFR-01 | Tolerate sensor failure/timeout | `SensorManager._safe_read` | `test_failing_sensor...` |
| NFR-02 | Type-safe, lint-clean | mypy strict, ruff, black | CI |
