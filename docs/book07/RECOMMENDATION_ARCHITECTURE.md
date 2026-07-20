# Recommendation Architecture

The Recommendation layer acts as the final orchestrator in the pipeline, consuming DTOs from matching and scoring layers to formulate structured resume intelligence.

## Recommendation Engine Pipeline

```
Upstream DTOs (MatchResult, ScoreResult, ExplainabilityResult)
       │
       ▼
RecommendationEngine.recommend()
       │
       ├──► RecommendationValidator.validate_inputs()
       ├──► RecommendationValidator.validate_registry()
       │
       ├──► Registered Providers (Sorted by priority ascending)
       │        ├── provider.validate()
       │        └── provider.generate()
       │
       ├──► Collate Recommendations
       │
       ├──► RecommendationStatisticsBuilder.build()
       │
       └──► Wrap into immutable RecommendationResult DTO
```
