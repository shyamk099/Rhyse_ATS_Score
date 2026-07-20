# Aggregator Class Diagram

```
┌──────────────────────────────────────────────┐
│            OverallScoreAggregator            │
├──────────────────────────────────────────────┤
│ - _weight_config: SectionWeightConfiguration │
│ - _last_aggregation_stats: dict              │
├──────────────────────────────────────────────┤
│ + aggregate(ScoreResult) → ScoreResult       │
│ + weight_config: SectionWeightConfiguration  │
│ + last_aggregation_stats: dict               │
└──────────────────────────────────────────────┘
           │ uses                    │ uses
           ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│   ScoreNormalizer   │   │    AggregationValidator     │
├─────────────────────┤   ├─────────────────────────────┤
│ + normalize()       │   │ + validate(result, weights) │
│ + normalize_all()   │   └─────────────────────────────┘
└─────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│    SectionWeightConfiguration    │
├──────────────────────────────────┤
│ + skill: float                   │
│ + experience: float              │
│ + education: float               │
│ + project: float                 │
│ + certification: float           │
│ + version: str                   │
├──────────────────────────────────┤
│ + validate_weights_sum()         │
│ + as_dict()                      │
└──────────────────────────────────┘

Exception Hierarchy:
  ScoringError
    └── AggregationError
          ├── NormalizationError
          ├── WeightConfigurationError
          └── AggregationValidationError
```
