# Orchestrator Package Diagram

```
ats_engine
└── domain
    └── ats_scoring                    ← Package boundary (__init__.py)
        ├── orchestrator/              ← NEW: Milestone 6.7
        │   ├── __init__.py
        │   ├── orchestrator.py        ← ScoreOrchestrator
        │   ├── execution_plan.py      ← ExecutionPlan, ExecutionPlanEntry
        │   ├── validator.py           ← ScoreOrchestratorValidator
        │   └── statistics_builder.py  ← OrchestratorStatisticsBuilder
        │
        ├── skill/                     ← Milestone 6.2
        ├── experience/                ← Milestone 6.3
        ├── education/                 ← Milestone 6.4
        ├── project/                   ← Milestone 6.5
        ├── certification/             ← Milestone 6.6
        │
        ├── common/                    ← Shared builders and validators
        ├── models/                    ← DTOs (ScoreResult, SectionScore, etc.)
        ├── pipeline.py                ← ScoringPipeline (existing)
        ├── registry.py                ← ScoringRegistry (existing)
        ├── factory.py                 ← ScoringFactory + create_default_orchestrator()
        ├── exceptions.py              ← + OrchestrationError, ExecutionPlanError,
        │                                  RegistryValidationError
        └── __init__.py                ← Exports all public symbols
```
