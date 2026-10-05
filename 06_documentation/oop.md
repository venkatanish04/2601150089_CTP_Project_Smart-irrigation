# Object-Oriented Programming (OOP) Design

## 1. Class Hierarchy & Polymorphism
```
              <<interface>>
                Scheduler
             (abstractmethod:
           generate_schedule)
                   ▲
         ┌─────────┴─────────┐
         │                   │
  GreedyScheduler       DPScheduler
```

Both `GreedyScheduler` and `DPScheduler` inherit from `Scheduler`. Polymorphic invocation allows the `IrrigationSystem` to execute:
```python
chosen_candidates = self.scheduler.generate_schedule(candidates, budget)
```
without knowing whether Greedy or DP is active.

## 2. Encapsulation & Composition
The `IrrigationSystem` does not inherit from sensors, weather providers, or schedulers. Instead, it composes them:
- `self.sensor_manager: SensorManager`
- `self.weather_service: WeatherService`
- `self.scheduler: Scheduler`

This guarantees that each component can be independently tested, mocked, or replaced without side effects.
