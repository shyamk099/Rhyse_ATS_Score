# Certification Provider Architecture

The `CertificationRecommendationProvider` implements the abstract `BaseRecommendationProvider` interface. It decouples rules, builder, validator, and statistics builder.

## Flow Architecture

```
RecommendationContext DTO
       │
       ▼
CertificationRecommendationProvider.generate()
       │
       ├──► validate() inputs
       │
       ├──► Parse Missing Certifications (ScoreBreakdown.missing_items)
       │        └── CertificationRecommendationRules.evaluate_missing()
       │                 └── CertificationRecommendationBuilder.build_missing_recommendation()
       │
       ├──► Parse Matched Certifications (MatchResult.custom_attributes)
       │        └── CertificationRecommendationRules.evaluate_match()
       │                 ├── PARTIAL ─► build_partial_recommendation()
       │                 └── EXPIRED ─► build_expired_recommendation()
       │
       ├──► CertificationRecommendationValidator.validate()
       │
       └──► CertificationRecommendationStatisticsBuilder.build()
```
