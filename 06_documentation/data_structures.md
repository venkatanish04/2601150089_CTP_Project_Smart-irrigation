# Data Structures Selection & Justification

| Data Structure | Implementation | Why Selected? | Computational Complexity |
|---|---|---|---|
| **Hash Map / Dict** | `dict[str, SoilReading]` | Key-value lookup of sensor readings indexed by `field_id`. | $\mathcal{O}(1)$ average insertion and lookup. |
| **Priority Queue / Min-Heap** | `heapq` in `UrgentQueue` | Efficient retrieval of candidate fields ordered by urgency benefit. Stored as negated floats to implement a max-heap. | $\mathcal{O}(\log n)$ insertion and extraction. |
| **Dynamic Array / List** | `list[Candidate]`, `list[ScheduleEntry]` | Ordered collection of candidates and sequential schedule time slots. | $\mathcal{O}(1)$ append, $\mathcal{O}(n)$ iteration. |
| **Set** | `set[str]` in `validate()` & `IrrigationController` | Detecting duplicate field allocations and tracking actively open physical solenoid valves. | $\mathcal{O}(1)$ average membership test. |
| **2D Matrix / Table** | `list[list[float]]` in `dynamic_schedule` | Tabulation table for the 0/1 knapsack dynamic programming state. | $\mathcal{O}(nW)$ space and $\mathcal{O}(1)$ cell access. |
| **Frozen Dataclass** | `@dataclass(frozen=True)` | Domain models (`Field`, `SoilReading`, `Candidate`, `WeatherForecast`). Immutable value objects guarantee thread safety. | $\mathcal{O}(1)$ instantiation. |
