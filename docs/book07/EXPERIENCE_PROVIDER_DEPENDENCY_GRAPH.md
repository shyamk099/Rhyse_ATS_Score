# Experience Provider Dependency Graph

```
ExperienceRecommendationProvider
    ├── BaseRecommendationProvider        (recommendation.providers.base)
    ├── ExperienceRecommendationRules     (recommendation.providers.experience_rules)
    ├── ExperienceRecommendationBuilder   (recommendation.providers.experience_builder)
    ├── ExperienceRecommendationValidator (recommendation.providers.experience_validator)
    └── ExperienceRecommendationStatisticsBuilder (recommendation.providers.experience_statistics_builder)

RecommendationFactory
    └── create_default_recommendation_engine()
            └── ExperienceRecommendationProvider
```
