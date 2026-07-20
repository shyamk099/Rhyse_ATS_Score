# Certification Provider Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── providers/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── certification_provider.py       ← Concrete implementation
        │   ├── certification_rules.py          ← Rule action evaluation class
        │   ├── certification_builder.py        ← Deterministic construction
        │   ├── certification_validator.py      ← Validation checks
        │   └── certification_statistics_builder.py ← Telemetry stats
        │
        └── factory.py                          ← Registered inside factory
```
