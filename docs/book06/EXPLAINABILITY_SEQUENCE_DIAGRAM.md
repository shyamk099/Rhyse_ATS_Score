# Explainability Sequence Diagram

```
Client               ExplainabilityEngine      Validator / Checks    Formatter      Result DTO
  │                            │                       │                 │              │
  │  explain(score_result)     │                       │                 │              │
  │───────────────────────────►│                       │                 │              │
  │                            │ Validate ScoreResult  │                 │              │
  │                            │──────────────────────►│                 │              │
  │                            │◄──────────────────────│                 │              │
  │                            │                                         │              │
  │                            │ Format section formulas & summaries     │              │
  │                            │────────────────────────────────────────►│              │
  │                            │◄────────────────────────────────────────│              │
  │                            │                                         │              │
  │                            │ Format overall formula & summary (optional)            │
  │                            │────────────────────────────────────────►│              │
  │                            │◄────────────────────────────────────────│              │
  │                            │                                                        │
  │                            │ Construct DTO wrapper                                  │
  │                            │───────────────────────────────────────────────────────►│
  │                            │◄───────────────────────────────────────────────────────│
  │  return ExplainabilityResult                                                        │
  │◄───────────────────────────│                                                        │
```
