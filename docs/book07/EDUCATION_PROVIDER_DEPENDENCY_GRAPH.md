# Education Provider Dependency Graph

```
EducationRecommendationProvider
    ├── BaseRecommendationProvider        (recommendation.providers.base)
    ├── EducationRecommendationRules      (recommendation.providers.education_rules)
    ├── EducationRecommendationBuilder    (recommendation.providers.education_builder)
    ├── EducationRecommendationValidator  (recommendation.providers.education_validator)
    └── EducationRecommendationStatisticsBuilder (recommendation.providers.education_statistics_builder)

RecommendationFactory
    └── create_default_recommendation_engine()
            └── EducationRecommendationProvider
```
