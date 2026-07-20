# Experience Provider Architecture

The `ExperienceRecommendationProvider` implements the abstract `BaseRecommendationProvider` interface. It decouples rules, builder, validator, and statistics builder.

## Flow Architecture

```
RecommendationContext DTO
       │
       ▼
ExperienceRecommendationProvider.generate()
       │
       ├──► validate() inputs
       │
       ├──► Parse Missing Experience (ScoreBreakdown.missing_items)
       │        └── ExperienceRecommendationRules.evaluate_missing()
       │                 └── ExperienceRecommendationBuilder.build_missing_recommendation()
       │
       ├──► Parse Matched Experience (MatchResult.custom_attributes)
       │        └── ExperienceRecommendationRules.evaluate_match()
       │                 ├── PARTIAL ────► build_partial_recommendation()
       │                 └── DURATION_GAP ─► build_duration_gap_recommendation()
       │
       ├──► ExperienceRecommendationValidator.validate()
       │
       └──► ExperienceRecommendationStatisticsBuilder.build()
```
