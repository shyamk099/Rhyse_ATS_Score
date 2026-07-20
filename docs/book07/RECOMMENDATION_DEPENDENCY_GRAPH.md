# Recommendation Dependency Graph

```
RecommendationEngine
    ├── RecommendationRegistry            (recommendation.registry)
    ├── RecommendationValidator           (recommendation.validator)
    ├── RecommendationStatisticsBuilder   (recommendation.statistics_builder)
    └── RecommendationMetadataBuilder     (recommendation.metadata_builder)

RecommendationRegistry
    └── BaseRecommendationProvider        (recommendation.providers.base)

RecommendationFactory
    └── create_default_recommendation_engine()
            ├── RecommendationRegistry
            └── RecommendationEngine(registry)

Exceptions (clean boundaries):
    RecommendationError
        ├── RecommendationValidationError
        └── RecommendationProviderError
```
