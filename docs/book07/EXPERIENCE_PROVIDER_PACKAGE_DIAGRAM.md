# Experience Provider Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── providers/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── experience_provider.py           ← Concrete implementation
        │   ├── experience_rules.py              ← Rule action evaluation class
        │   ├── experience_builder.py            ← Deterministic construction
        │   ├── experience_validator.py          ← Validation checks
        │   └── experience_statistics_builder.py ← Telemetry stats
        │
        └── factory.py                           ← Registered inside factory
```
