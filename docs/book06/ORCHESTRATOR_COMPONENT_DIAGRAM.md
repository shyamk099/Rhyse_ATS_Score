# Orchestrator Component Diagram

```
┌───────────────────────────────────────────────────────────┐
│           domain/ats_scoring/orchestrator/                │
│                                                           │
│  ┌─────────────────┐    ┌──────────────────────────────┐  │
│  │  orchestrator.py│    │     execution_plan.py        │  │
│  │  ScoreOrchestrator│◄──│  ExecutionPlan               │  │
│  └────────┬────────┘    │  ExecutionPlanEntry          │  │
│           │              └──────────────────────────────┘  │
│           │ uses                                            │
│  ┌────────▼────────┐    ┌──────────────────────────────┐  │
│  │   validator.py  │    │   statistics_builder.py      │  │
│  │ ScoreOrch       │    │ OrchestratorStatisticsBuilder│  │
│  │ estratorValidator│    └──────────────────────────────┘  │
│  └─────────────────┘                                       │
└───────────────────────────────────────────────────────────┘
          │ depends on
          ▼
┌───────────────────────────────────────────────────────────┐
│          domain/ats_scoring/ (existing framework)          │
│  ScoringPipeline  ScoringRegistry  ScoringFactory          │
│  ScoringRules     ScoreResult      ScoreStatistics         │
│  SectionScore     ScoreBreakdown   ScoreMetadata           │
└───────────────────────────────────────────────────────────┘
