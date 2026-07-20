# Project Provider Architecture

The `ProjectRecommendationProvider` implements the abstract `BaseRecommendationProvider` interface. It decouples rules, builder, validator, and statistics builder.

## Flow Architecture

```
RecommendationContext DTO
       │
       ▼
ProjectRecommendationProvider.generate()
       │
       ├──► validate() inputs
       │
       ├──► Parse Missing Projects (ScoreBreakdown.missing_items)
       │        └── ProjectRecommendationRules.evaluate_missing()
       │                 └── ProjectRecommendationBuilder.build_missing_recommendation()
       │
       ├──► Parse Matched Projects (MatchResult.custom_attributes)
       │        └── ProjectRecommendationRules.evaluate_match()
       │                 ├── PARTIAL ────► build_partial_recommendation()
       │                 └── RELATED_GAP ─► build_related_gap_recommendation()
       │
       ├──► ProjectRecommendationValidator.validate()
       │
       └──► ProjectRecommendationStatisticsBuilder.build()
```
