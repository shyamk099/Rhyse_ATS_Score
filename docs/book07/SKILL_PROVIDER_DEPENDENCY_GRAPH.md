# Skill Provider Dependency Graph

```
SkillRecommendationProvider
    ├── BaseRecommendationProvider        (recommendation.providers.base)
    ├── SkillRecommendationRules          (recommendation.providers.skill_rules)
    ├── SkillRecommendationBuilder        (recommendation.providers.skill_builder)
    ├── SkillRecommendationValidator      (recommendation.providers.skill_validator)
    └── SkillRecommendationStatisticsBuilder (recommendation.providers.skill_statistics_builder)

RecommendationFactory
    └── create_default_recommendation_engine()
            └── SkillRecommendationProvider
```
