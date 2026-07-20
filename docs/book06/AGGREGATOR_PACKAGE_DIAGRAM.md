# Aggregator Package Diagram

```
ats_engine
└── domain
    └── ats_scoring                    ← Package boundary
        ├── aggregation/               ← NEW: Milestone 6.8
        │   ├── __init__.py
        │   ├── aggregator.py          ← OverallScoreAggregator
        │   ├── weighting.py           ← SectionWeightConfiguration
        │   ├── normalization.py       ← ScoreNormalizer
        │   ├── validator.py           ← AggregationValidator
        │   └── statistics_builder.py  ← AggregationStatisticsBuilder
        │
        ├── orchestrator/              ← Milestone 6.7
        ├── skill/                     ← Milestone 6.2
        ├── experience/                ← Milestone 6.3
        ├── education/                 ← Milestone 6.4
        ├── project/                   ← Milestone 6.5
        ├── certification/             ← Milestone 6.6
        └── factory.py                 ← scoring factory + default aggregator
```
