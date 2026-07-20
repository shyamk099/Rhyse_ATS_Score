# Book 07 — Resume Intelligence Engine
# Milestone 7.7 — Recommendation Prioritization Engine

## Overview
Milestone 7.7 delivers the **Recommendation Prioritization Engine**, which processes generated recommendation DTOs, assigns deterministic priority, impact, and confidence fields, sorts them, and compiles execution statistics.

## Scope
This engine is a post-processing stage.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| PrioritizedRecommendationResult | Heuristic or probabilistic ranking |
| PriorityKey lookup mappings | AI / LLM / embeddings |
| PrioritizationRules & PriorityProfiles | Resumes rewriting |
| PrioritizationBuilder & validator | Mutating original recommendation IDs |
| Pipeline integration (PostProcessors) | Unsorted recommendations output |

## Pipeline Flow
```
[Providers]
   │
   ▼
[RecommendationResult]
   │
   ▼
[PostProcessor Stage: PrioritizationEngine]
   │  └── Rules / Profile lookup by PriorityKey
   │  └── Sort DTOs (priority DESC, impact DESC, ID ASC)
   │  └── Validate ranges and sorting constraints
   │  └── Compile PrioritizationStatistics DTO
   ▼
[PrioritizedRecommendationResult]
```
