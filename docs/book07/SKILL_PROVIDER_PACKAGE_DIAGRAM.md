# Skill Provider Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── providers/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── skill_provider.py           ← Concrete implementation
        │   ├── skill_rules.py              ← Rule decision class
        │   ├── skill_builder.py            ← Construction logic helper
        │   ├── skill_validator.py          ← Constraint validator
        │   └── skill_statistics_builder.py ← Performance metric builder
        │
        └── factory.py                      ← Registered inside RecommendationFactory
```
