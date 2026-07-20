# Education Provider Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── providers/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── education_provider.py           ← Concrete implementation
        │   ├── education_rules.py              ← Rule action evaluation class
        │   ├── education_builder.py            ← Deterministic construction
        │   ├── education_validator.py          ← Validation checks
        │   └── education_statistics_builder.py ← Telemetry stats
        │
        └── factory.py                          ← Registered inside factory
```
