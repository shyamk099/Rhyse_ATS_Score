# Prioritization Dependency Graph

```
PrioritizationEngine (domain.recommendation.prioritization.prioritization_engine)
    ├── BasePostProcessor (domain.recommendation.post_processors.base)
    ├── PrioritizedRecommendationResult (domain.recommendation.prioritization.models)
    ├── PrioritizationRules (domain.recommendation.prioritization.prioritization_rules)
    ├── PrioritizationBuilder (domain.recommendation.prioritization.prioritization_builder)
    ├── PrioritizationValidator (domain.recommendation.prioritization.prioritization_validator)
    └── PrioritizationStatisticsBuilder (domain.recommendation.prioritization.prioritization_statistics_builder)

RecommendationEngine
    └── recommend()
            └── loops and executes post_processors list
```
