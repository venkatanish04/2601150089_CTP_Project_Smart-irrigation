# Data Flow Architecture

The end-to-end data lifecycle flows through distinct transformation stages:

```
[ In-Ground Sensors ]       [ Weather API/Model ]
         │                            │
         │ (asyncio.gather)           │ (async read)
         ▼                            ▼
  SoilReadings Dict           WeatherForecast
         │                            │
         └─────────────┬──────────────┘
                       ▼
            [ build_candidates() ]
                       │
       ┌───────────────┴───────────────┐
       │ (Filter: moisture < threshold)│
       │ (Apply: weather_adjustment)   │
       │ (Round: math.ceil(litres))    │
       │ (Score: calculate_benefit)    │
       └───────────────┬───────────────┘
                       ▼
            List of Candidate Objects
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[ Greedy Algorithm ]       [ 0/1 Knapsack DP ]
  Sort by benefit/water      Construct 2D DP matrix
  Greedy selection           Backtrack optimal set
         │                           │
         └─────────────┬─────────────┘
                       ▼
            Selected Candidates List
                       │
                       ▼
            [ build_schedule() ]
                       │
       ┌───────────────┴───────────────┐
       │ - Assign chronological start  │
       │ - Compute cumulative water    │
       │ - Assert water <= budget      │
       │ - Compute total benefit score │
       └───────────────┬───────────────┘
                       ▼
               Schedule Object
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
[ CLI Dashboard ]  [ Disk Log ]  [ Valve Relays ]
```

### Stage Details
1. **Telemetry Sampling**: Soil readings (`moisture`, `temperature`, `humidity`) collected concurrently via `asyncio.gather`.
2. **Deficit & Candidate Transformation**: Fields whose moisture is already adequate ($\ge \text{threshold}$) are pruned. Remaining fields have water requirement reduced proportionally to rain probability:
   $$\text{Water} = \lceil \text{WaterReq} \times \left(1 - \frac{\text{Moisture}}{\text{Threshold}}\right) \times \left(1 - \frac{\text{RainProb}}{100}\right) \rceil$$
3. **Constrained Optimization**: Candidate set and available budget ($W$) are submitted to the active `Scheduler`.
4. **Plan Assembly & Verification**: Selected fields are sequenced in order of priority and assigned 20-minute execution windows. `schedule.validate()` asserts total water $\le W$ and verifies field IDs are unique.
