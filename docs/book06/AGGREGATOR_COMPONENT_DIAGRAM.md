# Aggregator Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│             domain/ats_scoring/aggregation/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │      aggregator.py      │    │      normalization.py   │  │
│  │  OverallScoreAggregator │───►│  ScoreNormalizer        │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │      validator.py       │    │      weighting.py       │  │
│  │  AggregationValidator   │    │  SectionWeightConfig    │  │
│  └─────────────────────────┘    └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
          │ depends on
          ▼
┌──────────────────────────────────────────────────────────────┐
│           domain/ats_scoring/ (models & core)                │
│  ScoreResult  SectionScore  ScoringFactory  ScoringRules     │
└──────────────────────────────────────────────────────────────┘
```
