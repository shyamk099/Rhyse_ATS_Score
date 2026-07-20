# Skill Provider Architecture

The `SkillRecommendationProvider` implements the abstract `BaseRecommendationProvider` interface. It decouples rules, builder, validator, and statistics builder.

## Flow Architecture

```
RecommendationContext DTO
       │
       ▼
SkillRecommendationProvider.generate()
       │
       ├──► validate() inputs
       │
       ├──► Parse Missing Skills (ScoreBreakdown.missing_items)
       │        └── SkillRecommendationRules.should_recommend("SKILL_MISSING")
       │                 └── SkillRecommendationBuilder.build_missing_recommendation()
       │
       ├──► Parse Partially Matched Skills (MatchResult.custom_attributes)
       │        └── SkillRecommendationRules.should_recommend("SKILL_PARTIAL_MATCH")
       │                 └── SkillRecommendationBuilder.build_partial_recommendation()
       │
       ├──► SkillRecommendationValidator.validate()
       │
       └──► SkillRecommendationStatisticsBuilder.build()
```
