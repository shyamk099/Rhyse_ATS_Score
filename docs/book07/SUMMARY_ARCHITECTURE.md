# Summary Architecture

## Layered Pipeline

```
RecommendationEngine.recommend(context)
    │
    ▼
Providers (Skill, Experience, Education, Project, Certification)
    │
    ▼
PrioritizationEngine (BasePostProcessor)
    │  Assigns priority, impact, confidence
    ▼
RecommendationOrchestrationEngine (BasePostProcessor)
    │  Groups by section, category, priority tier
    ▼
ResumeIntelligenceSummaryEngine (BasePostProcessor)
    │  Compiles health, section summaries, top recommendations
    ▼
ResumeIntelligenceSummary (Final Output)
```

## Design Principles

1. **One-directional dependency graph** — No stage reaches backwards.
2. **Separation of policy and construction** — `ResumeHealthPolicy` is isolated from `ResumeSummaryBuilder`.
3. **Consumer, not decision maker** — The summary engine never re-sorts, re-filters, or re-computes.
4. **Immutable DTOs** — All outputs are frozen Pydantic models.
5. **Deterministic** — Identical inputs always produce identical outputs.

## Input/Output Contract

| Property | Value |
|---|---|
| Input | `OrchestratedRecommendationResult` |
| Output | `ResumeIntelligenceSummary` |
| Side Effects | None |
| Mutability | Immutable |
| Thread Safety | Yes |
