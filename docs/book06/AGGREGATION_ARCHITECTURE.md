# Aggregation Architecture

The Aggregation layer is decoupled from scoring logic. It operates purely as a data-transformation layer on top of a completed `ScoreResult`.

## Data Pipeline Flow

```
Completed ScoreResult (overall_score=None)
       │
       ▼
OverallScoreAggregator.aggregate()
       │
       ├──► AggregationValidator.validate()
       │        └── AggregationValidationError on failure
       │
       ├──► ScoreNormalizer.normalize_all()
       │        ├── (raw / max) * 100 per section
       │        └── NormalizationError if maximum_score is 0/None
       │
       ├──► Weighted Average Calculation
       │        └── Apply SectionWeightConfiguration weights
       │
       ├──► Clamping [0.0, 100.0]
       │
       ├──► AggregationStatisticsBuilder.build()
       │
       └──► result.model_copy(update={"overall_score": overall_score})
                └── Returns new immutable ScoreResult DTO
```
