# Explainability Package Diagram

```
ats_engine
└── domain
    └── ats_scoring                    ← Package boundary
        ├── explainability/            ← NEW: Milestone 6.9
        │   ├── __init__.py
        │   ├── explainer.py           ← ExplainabilityEngine
        │   ├── models.py              ← DTO models
        │   ├── formatter.py           ← ExplainabilityFormatter
        │   ├── metadata_builder.py    ← Metadata compiler
        │   └── statistics_builder.py  ← Statistics compiler
        │
        ├── aggregation/               ← Milestone 6.8
        ├── orchestrator/              ← Milestone 6.7
        ├── skill/                     ← Milestone 6.2
        ├── experience/                ← Milestone 6.3
        ├── education/                 ← Milestone 6.4
        ├── project/                   ← Milestone 6.5
        ├── certification/             ← Milestone 6.6
        └── factory.py                 ← scoring factory + default explainer
```
