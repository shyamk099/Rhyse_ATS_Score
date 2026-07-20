# Education Provider Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/recommendation/providers/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ education_provider.py   │───►│   education_rules.py    │  │
│  │ EducationRecommendProv  │    │ EducationRecommendRules │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ education_builder.py    │    │ education_validator.py  │  │
│  │ EducationRecommendBuild │    │ EducationRecommendValid │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ education_stati...py    │                                 │
│  │ EducationRecommendStats │                                 │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
