# Orchestrator Dependency Graph

```
ScoreOrchestrator
    ├── ScoringPipeline           (ats_scoring.pipeline)
    │       └── ScoringRegistry   (ats_scoring.registry)
    │           ├── SkillScorer
    │           ├── ExperienceScorer
    │           ├── EducationScorer
    │           ├── ProjectScorer
    │           └── CertificationScorer
    │
    ├── ScoringRegistry           (ats_scoring.registry)
    │
    ├── ExecutionPlan             (orchestrator.execution_plan)
    │       └── ExecutionPlanEntry (NamedTuple)
    │
    ├── ScoreOrchestratorValidator (orchestrator.validator)
    │
    ├── OrchestratorStatisticsBuilder (orchestrator.statistics_builder)
    │
    └── ScoringRules              (ats_scoring.rules) [default fallback]

ScoringFactory
    └── create_default_orchestrator()
            ├── create_default_registry()
            ├── create_default_pipeline()
            └── ScoreOrchestrator(pipeline, registry)

Exceptions (no circular deps):
    ScoringError
        └── OrchestrationError
              ├── ExecutionPlanError    (raised by ExecutionPlan.build)
              └── RegistryValidationError (raised by ScoreOrchestratorValidator)
```
