# Skill Provider Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/recommendation/providers/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │    skill_provider.py    │───►│     skill_rules.py      │  │
│  │ SkillRecommendationProv │    │ SkillRecommendationRules│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │    skill_builder.py     │    │   skill_validator.py    │  │
│  │ SkillRecommendationBuild│    │ SkillRecommendationValid│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ skill_statistics_...py  │                                 │
│  │ SkillRecommendationStats│                                 │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
