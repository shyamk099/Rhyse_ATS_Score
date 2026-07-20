# Certification Provider Dependency Graph

```
CertificationRecommendationProvider
    ├── BaseRecommendationProvider        (recommendation.providers.base)
    ├── CertificationRecommendationRules  (recommendation.providers.certification_rules)
    ├── CertificationRecommendationBuilder (recommendation.providers.certification_builder)
    ├── CertificationRecommendationValidator (recommendation.providers.certification_validator)
    └── CertificationRecommendationStatisticsBuilder (recommendation.providers.certification_statistics_builder)

RecommendationFactory
    └── create_default_recommendation_engine()
            └── CertificationRecommendationProvider
```
