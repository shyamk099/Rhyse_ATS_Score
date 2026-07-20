# Project Provider Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/recommendation/providers/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ project_provider.py     │───►│    project_rules.py     │  │
│  │ ProjectRecommendationPro│    │ ProjectRecommendationRul│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ project_builder.py      │    │ project_validator.py    │  │
│  │ ProjectRecommendationBld│    │ ProjectRecommendationVal│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ project_stati...py      │                                 │
│  │ ProjectRecommendationSta│  │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
