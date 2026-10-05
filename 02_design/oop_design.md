# Object-Oriented Design & Patterns

## 1. Core Object-Oriented Principles
The system rigorously adheres to SOLID design principles:

### Single Responsibility Principle (SRP)
- `SensorManager` is solely responsible for polling and managing network timeouts.
- `WeatherService` is solely responsible for meteorological data acquisition.
- `Scheduler` is solely responsible for constrained combinatorial selection.
- `IrrigationSystem` coordinates business logic across domain components.

### Open-Closed Principle (OCP)
New scheduling algorithms (e.g., Integer Linear Programming, Simulated Annealing, Genetic Algorithms) can be introduced by subclassing `Scheduler` without altering existing application code.

### Liskov Substitution Principle (LSP)
`GreedyScheduler` and `DPScheduler` are completely interchangeable wherever `Scheduler` is expected.

### Interface Segregation Principle (ISP)
Interfaces (`Sensor`, `WeatherService`, `Scheduler`) are lean, focused, and define only the minimal required contract.

### Dependency Inversion Principle (DIP)
High-level modules depend on abstractions (e.g., `IrrigationSystem` depends on `Scheduler` ABC, not concrete classes).

---

## 2. Design Patterns Applied

### 1. Strategy Pattern
Enables runtime algorithm selection:
```python
class Scheduler(ABC):
    @abstractmethod
    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        pass

class GreedyScheduler(Scheduler):
    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        return greedy_schedule(candidates, budget)

class DPScheduler(Scheduler):
    def generate_schedule(self, candidates: list[Candidate], budget: int) -> list[Candidate]:
        return dynamic_schedule(candidates, budget)
```

### 2. Composition over Inheritance
`IrrigationSystem` composes independent service objects rather than subclassing them:
```python
class IrrigationSystem:
    def __init__(
        self,
        fields: list[Field],
        sensor_manager: SensorManager,
        weather_service: WeatherService,
        scheduler: Scheduler,
        settings: Settings | None = None,
    ) -> None:
        self.fields = fields
        self.sensor_manager = sensor_manager
        self.weather_service = weather_service
        self.scheduler = scheduler
```

### 3. Immutable Domain Models (Value Objects)
Dataclasses are declared with `frozen=True` to guarantee thread-safe immutability.
