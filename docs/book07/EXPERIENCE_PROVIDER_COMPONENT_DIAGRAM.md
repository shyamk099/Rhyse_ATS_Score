# Experience Provider Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/recommendation/providers/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ experience_provider.py  │───►│  experience_rules.py    │  │
│  │ ExperienceRecommendProv │    │ ExperienceRecommendRules│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ experience_builder.py   │    │ experience_validator.py │  │
│  │ ExperienceRecommendBuild│    │ ExperienceRecommendValid│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ experience_stati...py   │                                 │
│  │ ExperienceRecommendStats│                                 │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
