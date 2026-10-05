# Verification & Validation Protocol for AI-Generated Code

To ensure academic and engineering rigor, all AI-assisted components are verified via a four-gate validation pipeline:

```
[ AI Code Generation ]
          │
          ▼
   [ Gate 1: Type Checking ]  ──> mypy --strict (0 errors required)
          │
          ▼
   [ Gate 2: Static Linting ] ──> ruff check & black --check (PEP 8 compliance)
          │
          ▼
   [ Gate 3: Unit & Edge ]    ──> pytest (boundary, negative, zero values)
          │
          ▼
   [ Gate 4: Property Tests ] ──> Hypothesis (fuzzing invariants, combinatorial equivalence)
          │
          ▼
   [ Verified & Accepted ]
```

## Formal Invariant Validation Matrix
1. **Budget Invariant**: For any randomly generated candidate list and budget $W \ge 0$, $\sum w_{\text{scheduled}} \le W$.
2. **Optimality Invariant**: For any inputs, $\text{Benefit}(\text{DP}) \ge \text{Benefit}(\text{Greedy}) - \epsilon$.
3. **Soundness Invariant**: For small inputs ($N \le 8$), $\text{Benefit}(\text{DP}) \equiv \text{Benefit}(\text{Brute Force})$.
4. **Idempotence / Uniqueness**: No candidate field is scheduled more than once in a cycle.
