# AI-assisted development log

Workflow: **specification first** (`docs/requirements.md`) -> constrained prompts -> generated code -> human review -> tests -> static analysis.

Example prompt: *"Design pure functions for irrigation need using dataclasses and type hints, no global state, return 0 when moisture >= threshold, raise ValueError on invalid input, no external dependencies, with pytest tests for normal, boundary and invalid inputs."*

Review checklist applied to every generated piece: satisfies requirement? algorithm correct? edge cases? tests pass? complexity acceptable? no needless dependencies? fits architecture?

Corrections made during review (record your own too):
1. Naive rule `if moisture < threshold: water = requirement` ignored the deficit -> replaced with proportional deficit formula.
2. Litres were first fractional; DP needs integer weights -> `math.ceil` so rounding never over-allocates.
3. Linter flagged blind `except Exception`; kept deliberately (one bad sensor must not stop a cycle) and documented why.
4. A sandbox with one CPU core showed no multiprocessing speedup; documented honestly rather than claiming one.
