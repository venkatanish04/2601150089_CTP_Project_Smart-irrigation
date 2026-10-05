# Algorithms

Problem: choose fields to irrigate maximising total benefit subject to `sum(water) <= budget` - a **0/1 knapsack**.

| | Greedy | Dynamic programming |
|---|---|---|
| Idea | sort by benefit/litre, take while it fits | `dp[i][w]` = best benefit with first i fields, w litres |
| Time | O(n log n) | O(n·W) |
| Space | O(n) | O(n·W) (table kept for reconstruction; reducible to O(W) if not reconstructing) |
| Optimal? | No (heuristic) | Yes, for integer litres |

DP recurrence: `dp[i][w] = max(dp[i-1][w], benefit[i] + dp[i-1][w - water[i]])`.
Water is rounded **up** to whole litres (`math.ceil`) so the discretisation can never over-allocate.

Counter-example where greedy loses (see `test_dp_beats_greedy_on_classic_case`): items (10 L, 60), (20 L, 100), (30 L, 120), budget 50.
Greedy takes the first two = 160; DP takes the last two = 220.

Other paradigms (divide & conquer, backtracking, branch & bound) were deliberately not forced into the design; DP is validated against brute-force enumeration in `tests/property`.
