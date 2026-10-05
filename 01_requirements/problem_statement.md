# Problem Statement: Smart Irrigation Scheduling System

## 1. Domain Background & Problem Context
Freshwater scarcity is one of the most critical global challenges facing modern agriculture. Agriculture accounts for roughly 70% of global freshwater withdrawals. Traditional irrigation systems operate on rudimentary fixed-time schedules (e.g., watering fields every day at 06:00 for 30 minutes).

### Key Flaws of Fixed-Schedule Irrigation:
1. **Severe Water Wastage**: Crops are irrigated even when soil moisture is already at or above saturation capacity.
2. **Ignorance of Weather Forecasts**: Fields are watered immediately prior to heavy rainfall events, causing nutrient runoff, soil erosion, and complete loss of pumped water.
3. **Depletion of Constrained Water Reservoirs**: During drought or peak dry seasons, local storage reservoirs have strict water volume limits. Indiscriminate early watering of low-priority zones leaves high-priority, drought-sensitive crops to wilt when reserves deplete.
4. **Lack of Real-Time Responsiveness**: Microclimates cause different plots to lose moisture at radically different rates depending on soil texture, crop species, and canopy exposure.

---

## 2. The Proposed Solution
The **Smart Irrigation Scheduling System** dynamically computes an optimal water distribution plan for a multi-zone agricultural network by synthesizing:
- Real-time soil moisture, temperature, and humidity telemetry from deployed in-ground sensors.
- Localized quantitative precipitation and temperature forecasts.
- Specific crop evapotranspiration coefficients and minimum moisture safety thresholds.
- Global water reserve budget constraints.

### Core Objectives:
- **Objective 1 (Water Conservation)**: Strictly eliminate irrigation when soil moisture exceeds threshold limits or when expected precipitation satisfies crop evapotranspiration needs.
- **Objective 2 (Urgency & Vulnerability Prioritization)**: Maximize total agricultural utility by allocating limited water to plots exhibiting the highest moisture deficit and highest economic/crop vulnerability.
- **Objective 3 (Strict Reservoir Budget Compliance)**: Formulate the allocation as a constrained optimization problem that never violates water availability limits.
- **Objective 4 (Low-Latency Concurrency)**: Collect field telemetry asynchronously to prevent network latency from blocking decision cycles.
- **Objective 5 (Algorithmic Optimality vs. Heuristic Speed)**: Provide both a mathematically optimal 0/1 Knapsack Dynamic Programming scheduler and a fast $\mathcal{O}(n \log n)$ Greedy density scheduler.
