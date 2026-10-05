# Critical Review of AI-Generated Code

Every generated code snippet underwent human inspection, static analysis, and unit testing.

## Discovered Flaws & Human Corrections

### Flaw 1: Binary Deficit Calculation
- **AI-Generated Code**:
  ```python
  if moisture < threshold:
      water_needed = water_requirement
  ```
- **Critical Flaw**: Ignored the continuous gradient of moisture deficit. A field at 34% moisture received the exact same water volume as a field at 5% moisture.
- **Human Correction**:
  ```python
  deficit = threshold - moisture
  return water_requirement * (deficit / threshold)
  ```

---

### Flaw 2: Continuous Weight Discretization in Knapsack DP
- **AI-Generated Code**:
  Used floating-point water quantities as matrix indices directly: `dp[i][int(water)]`.
- **Critical Flaw**: Truncating floating-point numbers with `int()` rounds down, which could result in scheduling more water than physically available.
- **Human Correction**:
  Used `math.ceil()` during candidate creation so every allocation is conservative and discretizes safely to integer indices without budget violation.

---

### Flaw 3: Blanket Exception Catching Flagged by Linter
- **Linter Warning**:
  Ruff flagged `except Exception:` as too broad in `_safe_read`.
- **Review Decision**:
  Deliberately retained the broad exception handling with an explicit justification: in physical IoT networks, sensors can raise arbitrary hardware, serial, network, or socket errors. One failing probe must never crash an agricultural irrigation cycle.
