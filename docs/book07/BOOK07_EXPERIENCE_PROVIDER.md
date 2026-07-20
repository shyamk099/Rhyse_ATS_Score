# Book 07 — Resume Intelligence Engine
# Milestone 7.3 — Experience Recommendation Provider

## Overview
Milestone 7.3 delivers the **Experience Recommendation Provider**, which implements the second concrete recommendation provider. It identifies missing experience requirements, partial experience matches, and duration gaps, and generates structured recommendation DTOs.

## Scope
This provider implements experience matching recommendation logic.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| ExperienceRecommendationProvider | Prioritizing recommendations |
| ExperienceRecommendationRules | Computing impact/confidence |
| ExperienceRecommendationBuilder | NLG / AI text formatting |
| ExperienceRecommendationValidator | Resume rewriting suggestions |
| ExperienceRecommendationStatisticsBuilder | Education/Project/Cert recommendations |

## Execution Flow
1. **Validation**: Confirms the `RecommendationContext` contains a valid `score_result` with `experience_score` populated.
2. **Missing Experience Extraction**: Extracts missing experiences list from `score_result.experience_score.breakdown.missing_items`.
3. **Matched Experience Evaluation**: Iterates over matching results for experience and resolves them using `rules.evaluate_match(match)`.
4. **Deterministic DTO construction**: Uses `ExperienceRecommendationBuilder` to generate deterministic IDs (e.g. `EXP_MISSING_MICROSERVICES`) and populated DTOs.
5. **Validator Verification**: Ensures no duplicates or empty values exist in the output list.
