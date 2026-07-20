# Explainability Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/ats_scoring/explainability/                │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │      explainer.py       │    │      formatter.py       │  │
│  │  ExplainabilityEngine   │───►│  ExplainabilityFormatter│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │        models.py        │    │    metadata_builder.py  │  │
│  │  DTOs: Result, Section  │    │  Metadata Builders      │  │
│  └─────────────────────────┘    └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
          │ depends on
          ▼
┌──────────────────────────────────────────────────────────────┐
│           domain/ats_scoring/ (models & aggregation)         │
│  ScoreResult  SectionScore  SectionWeightConfiguration       │
└──────────────────────────────────────────────────────────────┘
```
