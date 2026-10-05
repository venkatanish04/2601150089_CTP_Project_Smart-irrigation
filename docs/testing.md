# Testing strategy

| Level | Location | What it proves |
|---|---|---|
| Unit | `tests/unit` | pure functions, models, algorithms, sensors, utils, edge cases (zero budget, empty list, invalid input) |
| Integration | `tests/integration` | sensors -> needs -> weather -> scheduler -> schedule; runtime strategy swap |
| End-to-end | `tests/e2e` | real CLI session driven through the menu; `--demo` flag with log file |
| Property (Hypothesis) | `tests/property` | budget never exceeded; no duplicate fields; DP >= greedy; **DP == brute-force optimum**; need bounded; rain never increases water |

Commands: `pytest --cov=app --cov-report=term-missing`, `mypy app/`, `ruff check .`, `black --check .`.
Latest run: 60 passed, 99% coverage.
