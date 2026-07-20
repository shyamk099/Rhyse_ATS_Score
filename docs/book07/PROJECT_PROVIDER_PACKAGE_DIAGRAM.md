# Project Provider Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── providers/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── project_provider.py             ← Concrete implementation
        │   ├── project_rules.py                ← Rule action evaluation class
        │   ├── project_builder.py              ← Deterministic construction
        │   ├── project_validator.py            ← Validation checks
        │   └── project_statistics_builder.py   ← Telemetry stats
        │
        └── factory.py                          ← Registered inside factory
```
