# Project Provider Dependency Graph

```
ProjectRecommendationProvider
    ├── BaseRecommendationProvider        (recommendation.providers.base)
    ├── ProjectRecommendationRules         (recommendation.providers.project_rules)
    ├── ProjectRecommendationBuilder       (recommendation.providers.project_builder)
    ├── ProjectRecommendationValidator     (recommendation.providers.project_validator)
    └── ProjectRecommendationStatisticsBuilder (recommendation.providers.project_statistics_builder)

RecommendationFactory
    └── create_default_recommendation_engine()
            └── ProjectRecommendationProvider
```
