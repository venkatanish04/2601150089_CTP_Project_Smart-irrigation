# Performance results

Measured by `python -m app.main --benchmark` on a 1-core Linux sandbox (Python 3.12). Re-run on your machine and replace these figures before your defence; sleep-based sensor delays are 2-8 ms each.

```
==================================================================
SENSOR POLLING: sequential vs asyncio
==================================================================
 Sensors  Sequential(s)   Async(s)   Speedup
      10         0.0509     0.0079      6.4x
      25         0.1342     0.0081     16.5x
      50         0.2632     0.0088     29.8x
     100         0.5509     0.0087     63.1x
     500         2.8061     0.0131    215.0x

==================================================================
SCHEDULERS: Greedy vs Dynamic Programming
==================================================================
Fields=10  Budget=114 L
  Greedy : 0.000025s  water=  101  benefit=   545.86
  DP     : 0.001238s  water=  101  benefit=   545.86  peak mem=18 KiB
  Greedy benefit gap vs optimal: 0.00%
Fields=50  Budget=534 L
  Greedy : 0.000013s  water=  528  benefit=  3548.77
  DP     : 0.054829s  water=  534  benefit=  3559.81  peak mem=558 KiB
  Greedy benefit gap vs optimal: 0.31%
Fields=100  Budget=1047 L
  Greedy : 0.000029s  water= 1039  benefit=  7012.88
  DP     : 0.265483s  water= 1047  benefit=  7029.12  peak mem=2140 KiB
  Greedy benefit gap vs optimal: 0.23%
Fields=200  Budget=2121 L
  Greedy : 0.000049s  water= 2112  benefit= 13476.12
  DP     : 1.078004s  water= 2121  benefit= 13505.84  peak mem=8592 KiB
  Greedy benefit gap vs optimal: 0.22%

```

Takeaways:

* Async polling stays almost flat (~8-13 ms) while sequential polling grows linearly - the speedup grows with sensor count (215x at 500 sensors).
* Greedy is ~4 orders of magnitude faster than DP at 200 fields, but DP gains ~0.2-0.3% more benefit and uses the whole budget.
* DP memory grows as O(n*W) (8.6 MiB at 200 fields).
