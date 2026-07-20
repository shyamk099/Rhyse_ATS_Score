# Education Provider Architecture

The `EducationRecommendationProvider` implements the abstract `BaseRecommendationProvider` interface. It decouples rules, builder, validator, and statistics builder.

## Flow Architecture

```
RecommendationContext DTO
       │
       ▼
EducationRecommendationProvider.generate()
       │
       ├──► validate() inputs
       │
       ├──► Parse Missing Education (ScoreBreakdown.missing_items)
       │        └── EducationRecommendationRules.evaluate_missing()
       │                 └── EducationRecommendationBuilder.build_missing_recommendation()
       │
       ├──► Parse Matched Education (MatchResult.custom_attributes)
       │        └── EducationRecommendationRules.evaluate_match()
       │                 ├── PARTIAL ──► build_partial_recommendation()
       │                 └── LEVEL_GAP ─► build_level_gap_recommendation()
       │
       ├──► EducationRecommendationValidator.validate()
       │
       └──► EducationRecommendationStatisticsBuilder.build()
```
