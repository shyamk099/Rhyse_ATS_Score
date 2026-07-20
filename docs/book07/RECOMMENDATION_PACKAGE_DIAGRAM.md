# Recommendation Package Diagram

```
ats_engine
└── domain
    ├── recommendation/                ← NEW: Milestone 7.1
    │   ├── __init__.py
    │   ├── engine.py                  ← RecommendationEngine
    │   ├── models.py                  ← Recommendation & Result DTOs
    │   ├── registry.py                ← RecommendationRegistry
    │   ├── validator.py               ← RecommendationValidator
    │   ├── statistics_builder.py      ← Stats telemetry builder
    │   ├── metadata_builder.py        ← Metadata builder
    │   ├── factory.py                 ← Factory builder
    │   ├── exceptions.py              ← Framework exceptions
    │   └── providers/                 ← Provider subpackage
    │       ├── __init__.py
    │       └── base.py                ← BaseRecommendationProvider ABC
    │
    ├── matching/                      ← Book 05
    └── ats_scoring/                   ← Book 06
```
