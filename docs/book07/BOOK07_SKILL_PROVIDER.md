# Book 07 — Resume Intelligence Engine
# Milestone 7.2 — Skill Recommendation Provider

## Overview
Milestone 7.2 delivers the **Skill Recommendation Provider**, which implements the first concrete recommendation provider. It deterministic identifies missing and partially matched skills and generates structured recommendation DTOs.

## Scope
This provider implements skill matching logic.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| SkillRecommendationProvider | Prioritizing recommendations |
| SkillRecommendationRules | Computing impact/confidence |
| SkillRecommendationBuilder | NLG / AI text formatting |
| SkillRecommendationValidator | Resume rewriting suggestions |
| SkillRecommendationStatisticsBuilder | Experience/Education recommendations |

## Execution Flow
1. **Validation**: Confirms the `RecommendationContext` contains a valid `score_result` with `skill_score` populated.
2. **Missing Skills Extraction**: Extracts missing skills list from `score_result.skill_score.breakdown.missing_items`.
3. **Partial Matches Extraction**: Loops over `match_collection.results` looking for match results classified as `"SKILL_PARTIAL_MATCH"` or `"partial"` in custom attributes.
4. **Rules Application**: Invokes `should_recommend()` to check if a category should generate recommendations.
5. **Builder & Validator Execution**: Assembles DTOs using `SkillRecommendationBuilder` and asserts correctness with `SkillRecommendationValidator`.
6. **Telemetry & Collation**: Computes duration, counts, and workloads, compiling them into statistics.
