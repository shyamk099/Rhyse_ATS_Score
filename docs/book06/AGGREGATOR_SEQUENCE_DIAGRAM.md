# Aggregator Sequence Diagram

```
Client               OverallScoreAggregator      Validator       Normalizer       ScoreResult (DTO)
  │                            │                     │                │                   │
  │  aggregate(score_result)   │                     │                │                   │
  │───────────────────────────►│                     │                │                   │
  │                            │ validate(res, w)    │                │                   │
  │                            │────────────────────►│                │                   │
  │                            │◄────────────────────│                │                   │
  │                            │ normalize_all(res)  │                │                   │
  │                            │─────────────────────────────────────►│                   │
  │                            │◄─────────────────────────────────────│                   │
  │                            │ Calculate overall   │                │                   │
  │                            │ score & clamp       │                │                   │
  │                            │ model_copy(overall) │                │                   │
  │                            │─────────────────────────────────────────────────────────►│
  │                            │◄─────────────────────────────────────────────────────────│
  │  return ScoreResult (new)  │                     │                │                   │
  │◄───────────────────────────│                     │                │                   │
```
