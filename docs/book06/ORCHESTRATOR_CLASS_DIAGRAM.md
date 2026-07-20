# Orchestrator Class Diagram

```
┌──────────────────────────────────────────────┐
│               ScoreOrchestrator              │
├──────────────────────────────────────────────┤
│ + pipeline: ScoringPipeline                  │
│ + registry: ScoringRegistry                  │
│ + last_orchestration_stats: dict             │
├──────────────────────────────────────────────┤
│ + orchestrate(collection, rules) → ScoreResult│
│ - _extract_section_times(result) → dict      │
└──────────────────────────────────────────────┘
           │ uses                    │ uses
           ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│  ExecutionPlan      │   │ ScoreOrchestratorValidator   │
├─────────────────────┤   ├─────────────────────────────┤
│ entries: tuple      │   │ + validate(registry) → None  │
│ skipped: tuple      │   └─────────────────────────────┘
│ registry_names: tuple│
├─────────────────────┤
│ + build(registry)   │
│ + execution_order   │
│ + __len__           │
└─────────────────────┘
           │ contains
           ▼
┌─────────────────────┐
│ ExecutionPlanEntry  │  ← NamedTuple
├─────────────────────┤
│ name: str           │
│ scorer_cls: type    │
│ priority: int       │
└─────────────────────┘

┌───────────────────────────────────┐
│  OrchestratorStatisticsBuilder    │
├───────────────────────────────────┤
│ + build(...) → dict[str, Any]     │
└───────────────────────────────────┘

Exception Hierarchy:
  ScoringError
    └── OrchestrationError
          ├── ExecutionPlanError
          └── RegistryValidationError
```
