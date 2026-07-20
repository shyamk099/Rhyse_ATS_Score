# Book 07 — Resume Intelligence Summary

## Overview

The Resume Intelligence Summary Engine is the final post-processor in the Book 07 pipeline. It consumes the `OrchestratedRecommendationResult` produced by the Orchestration Engine and generates a deterministic, immutable `ResumeIntelligenceSummary`.

## Pipeline Position

```
Providers → Prioritization → Orchestration → Summary
```

No stage reaches backwards. The Summary Engine is a **consumer**, not a decision maker.

## Key Components

| Component | Responsibility |
|---|---|
| `ResumeHealthPolicy` | Deterministic health classification from high-priority counts |
| `ResumeSummaryBuilder` | Assembles summary DTO; delegates health to policy |
| `ResumeSummaryValidator` | Validates conservation, subsets, uniqueness |
| `ResumeIntelligenceStatisticsBuilder` | Compiles execution metrics |
| `ResumeIntelligenceSummaryEngine` | Orchestrates build → validate → return |

## Resume Health Policy

| High Priority Count | Score | Grade | Status |
|---|---|---|---|
| 0 | 100.0 | A | Excellent |
| 1–2 | 85.0 | B | Good |
| 3–5 | 70.0 | C | Needs Improvement |
| >5 | 50.0 | D | Critical |

## Top Recommendations

The first `N = 5` recommendations are sliced from the already-prioritized list. No re-sorting. No re-filtering. No re-computation.

## DTOs

- `ResumeSectionSummary` — Per-section priority counts
- `ResumeHealth` — Score, grade, status
- `ResumeIntelligenceStatistics` — Execution metrics
- `ResumeIntelligenceSummary` — Final Book 07 output

All DTOs are immutable (frozen Pydantic models with `extra="forbid"`).
