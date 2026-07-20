# Book 06 — ATS Scoring Engine
# Milestone 6.7 — Score Orchestration Engine

## Overview

Milestone 6.7 implements the **Score Orchestration Engine** — the coordination layer that sits above the
five section scorers and the `ScoringPipeline` to produce a complete, immutable `ScoreResult`.

## Scope

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| ScoreOrchestrator | Overall ATS Score |
| ExecutionPlan | Score Normalization |
| ScoreOrchestratorValidator | Weighting |
| OrchestratorStatisticsBuilder | Penalty Engine |
| Factory integration | Bonus Engine |
| Full test suite (60 tests) | Recommendations |
| 8 documentation files | Explainability / AI |

## What Was Built

### ScoreOrchestrator
The central coordination class. Accepts a `CanonicalMatchCollection` and `ScoringRules`,
runs pre-flight validation, builds an `ExecutionPlan`, delegates to the `ScoringPipeline`,
captures wall-clock orchestration statistics, and returns the pipeline's `ScoreResult` unmodified.

### ExecutionPlan
An immutable planning artefact that encapsulates:
- Priority-sorted (descending) enabled scorer entries
- A list of skipped (disabled) scorer names
- All registered scorer names for statistics

### ScoreOrchestratorValidator
Stateless pre-flight validator that checks:
- Registry is non-empty
- All scorer classes are valid `AbstractScorer` subclasses
- Enabled flags are booleans
- Enabled scorer priorities are unique (determinism guarantee)

### OrchestratorStatisticsBuilder
Compiles a plain `dict[str, Any]` capturing:
- `execution_time_ms` (wall-clock)
- `section_execution_times` (per-section, where available)
- `sections_executed`, `sections_skipped`, `failed_sections`
- `pipeline_version`, `success`

## Integration Points

- `ScoringFactory.create_default_orchestrator()` — factory entry point
- `ats_engine.domain.ats_scoring.__init__` — all symbols exported
- Exceptions: `OrchestrationError`, `ExecutionPlanError`, `RegistryValidationError`

## Test Coverage

60 tests across 10 test files. 0 failures. All edge cases covered.
