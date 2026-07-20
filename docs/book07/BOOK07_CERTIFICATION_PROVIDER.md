# Book 07 — Resume Intelligence Engine
# Milestone 7.6 — Certification Recommendation Provider

## Overview
Milestone 7.6 delivers the **Certification Recommendation Provider**, which identifies missing certification requirements, partial certification matches, and expired certifications, producing structured recommendation DTOs.

## Scope
This provider implements certification matching recommendation logic.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| CertificationRecommendationProvider | Prioritizing recommendations |
| CertificationRecommendationRules | Computing impact/confidence |
| CertificationRecommendationBuilder | NLG / AI text formatting |
| CertificationRecommendationValidator | Resume rewriting suggestions |
| CertificationRecommendationStatisticsBuilder | Any other sections |

## Execution Flow
1. **Validation**: Confirms the `RecommendationContext` contains a valid `score_result` with `certification_score` populated.
2. **Missing Certification Extraction**: Extracts missing certifications list from `score_result.certification_score.breakdown.missing_items`.
3. **Matched Certification Evaluation**: Iterates over matching results for certifications and resolves them using `rules.evaluate_match(match)`.
4. **Deterministic DTO construction**: Uses `CertificationRecommendationBuilder` to generate deterministic IDs (e.g. `CERT_MISSING_AWS_SAA`) following `<SECTION>_<ACTION>_<TARGET>`.
5. **Validator Verification**: Ensures no duplicates, section scoping matches `certification`, and correct categories exist.
