# Orchestration Architecture

## Layer Diagram

```
CanonicalMatchCollection
       │
       ▼
ScoreOrchestrator.orchestrate()
       │
       ├──► ScoreOrchestratorValidator.validate(registry)
       │        └── RegistryValidationError on failure
       │
       ├──► ExecutionPlan.build(registry)
       │        └── ExecutionPlanError on failure
       │
       ├──► ScoringPipeline.execute(match_collection, rules)
       │        ├── SkillScorer
       │        ├── ExperienceScorer
       │        ├── EducationScorer
       │        ├── ProjectScorer
       │        └── CertificationScorer
       │             └── ScoreResult (immutable)
       │
       └──► OrchestratorStatisticsBuilder.build(...)
                └── dict[str, Any] stored in orchestrator
```

## Key Design Decisions

1. **Orchestrator delegates — never executes scoring.**
   All scoring calculations remain inside section scorers. The orchestrator only coordinates.

2. **ExecutionPlan is a separate planning step.**
   Construction (sorted, validated) is decoupled from execution (pipeline).

3. **ScoreResult is never mutated.**
   The pipeline's result is returned as-is. The orchestrator holds stats in its own state.

4. **Priority ordering is descending (highest first).**
   Matches the `ScoringPipeline`'s existing ordering to ensure behavioural consistency.

5. **Statistics are a plain dict, not a new DTO.**
   Avoids model bloat at this milestone; a typed `OrchestratorStatistics` DTO can be
   introduced in a later milestone when its fields are stable.
