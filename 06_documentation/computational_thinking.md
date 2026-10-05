# Computational Thinking in Smart Irrigation

Computational thinking is the bedrock of this project, structured across the four classic pillars:

## 1. Decomposition
Breaking down an intractable agricultural dilemma into distinct, solvable software stages:
- **Telemetry Gathering**: In-situ sensor polling asynchronously decoupled from network waiting.
- **Meteorological Synthesis**: Rain forecast scaling.
- **Deficit & Priority Pruning**: Filtering non-critical fields to keep combinatorial candidate sets minimal.
- **Constrained Optimization**: Deciding the subset of plots to irrigate given strict volumetric limits.
- **Dispatch Scheduling**: Converting a set of chosen plots into a serialized timeline of valve actuations.

## 2. Pattern Recognition
Recognizing that the resource allocation problem under a fixed reservoir capacity is isomorphic to the **0/1 Knapsack Problem**:
- Item weight $\equiv$ Water required by field ($w_i$).
- Item value $\equiv$ Urgent benefit score ($v_i$).
- Knapsack capacity $\equiv$ Total reservoir water budget ($W$).

## 3. Abstraction
Creating generic contracts that isolate hardware and algorithmic specifics:
- `Sensor` ABC isolates whether data comes from physical RS485 soil probes, MQTT brokers, or random simulators.
- `WeatherService` ABC isolates whether weather comes from Open-Meteo, NOAA, or local weather stations.
- `Scheduler` ABC isolates whether the optimization algorithm is Greedy, Dynamic Programming, or Branch & Bound.

## 4. Algorithm Design
Selecting, implementing, and formally analyzing algorithms suited to constraints:
- **Greedy heuristic** when computation must occur on low-power IoT microcontrollers in microseconds.
- **Dynamic programming** when absolute mathematical optimality is mandated to prevent crop failure.
