# Prioritization Package Diagram

```
ats_engine
└── domain
    └── recommendation/
        ├── post_processors/
        │   ├── base.py                         ← PostProcessor boundary interface
        │   └── __init__.py
        │
        ├── prioritization/
        │   ├── models.py                       ← Prioritization DTOs
        │   ├── prioritization_engine.py        ← Coordinates pipeline stage
        │   ├── prioritization_rules.py         ← Rule configuration table
        │   ├── prioritization_builder.py       ← deterministic ordering logic
        │   ├── prioritization_validator.py     ← validates range & sequence
        │   └── prioritization_statistics_builder.py ← compiles statistics DTO
        │
        └── engine.py                           ← Core recommendation engine
```
