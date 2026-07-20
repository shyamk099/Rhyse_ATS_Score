# Book 07 — Resume Intelligence Engine
# Milestone 7.5 — Project Recommendation Provider

## Overview
Milestone 7.5 delivers the **Project Recommendation Provider**, which identifies missing project requirements, partial project matches, and related project gaps, producing structured recommendation DTOs.

## Scope
This provider implements project matching recommendation logic.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| ProjectRecommendationProvider | Prioritizing recommendations |
| ProjectRecommendationRules | Computing impact/confidence |
| ProjectRecommendationBuilder | NLG / AI text formatting |
| ProjectRecommendationValidator | Resume rewriting suggestions |
| ProjectRecommendationStatisticsBuilder | Certification recommendations |

## Execution Flow
1. **Validation**: Confirms the `RecommendationContext` contains a valid `score_result` with `project_score` populated.
2. **Missing Project Extraction**: Extracts missing projects list from `score_result.project_score.breakdown.missing_items`.
3. **Matched Project Evaluation**: Iterates over matching results for projects and resolves them using `rules.evaluate_match(match)`.
4. **Deterministic DTO construction**: Uses `ProjectRecommendationBuilder` to generate deterministic IDs (e.g. `PROJ_MISSING_MICROSERVICES`) following `<SECTION>_<ACTION>_<TARGET>`.
5. **Validator Verification**: Ensures no duplicates, section scoping matches `project`, and correct categories exist.
