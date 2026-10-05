# System Architecture & Layered Design

## 1. Architectural Overview
The Smart Irrigation Scheduling System is architected according to clean, modular, layered design principles. High-level concerns are strictly decoupled:

```
┌─────────────────────────────────────────────────────────────┐
│                 Presentation Layer (CLI)                    │
│      Interactive Dashboard • Renderers • Console Output     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  Service Orchestration Layer                │
│    IrrigationSystem • BenchmarkService • MonitoringService   │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼──────────────┐ ┌──────────────▼──────────────┐
│  Data Acquisition Layer     │ │   Algorithmic Decision Layer│
│  - SensorManager (asyncio)  │ │   - Pure Scoring Functions  │
│  - WeatherService           │ │   - Strategy Pattern:       │
│  - Sensor Simulators        │ │     * GreedyScheduler       │
│                             │ │     * DPScheduler           │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
┌──────────────▼───────────────────────────────▼──────────────┐
│                 Domain Models & Infrastructure              │
│       Frozen Dataclasses • Logging Context • Timing Decorator│
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Breakdown

1. **Telemetry & Sensor Subsystem**:
   - `Sensor` (Abstract Base Class) defines the hardware interface: `async def read() -> SoilReading`.
   - `SimulatedSensor` models realistic distributed network delays and telemetry variance.
   - `FailingSensor` models edge-case network dropouts to verify fault tolerance.
   - `SensorManager` manages concurrent polling with individual coroutine timeouts.

2. **Weather Intelligence Subsystem**:
   - `WeatherService` (ABC) with `SimulatedWeatherService` providing dynamic precipitation probability and expected rain depth.

3. **Domain Engine Subsystem**:
   - Pure functional calculations for moisture deficit, weather discounting, and multi-attribute benefit scores.

4. **Interchangeable Scheduling Engine**:
   - Strategy Pattern implementation allowing dynamic runtime swapping between `GreedyScheduler` and `DPScheduler`.

5. **Schedule Verification & Dispatch**:
   - Formulates sorted chronological time slots and verifies zero reservoir over-allocation.
