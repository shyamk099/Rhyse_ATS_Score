# Experience Provider Sequence Diagram

```
Engine            ExperienceRecommendationProvider   Rules      Builder      Validator      Stats
  │                            │                       │           │            │             │
  │  generate(context)         │                       │           │            │             │
  │───────────────────────────►│                       │           │            │             │
  │                            │ evaluate_missing/match│           │            │             │
  │                            │──────────────────────►│           │            │             │
  │                            │◄──────────────────────│           │            │             │
  │                            │                                   │            │             │
  │                            │ build_missing/partial/duration()  │            │             │
  │                            │──────────────────────────────────►│            │             │
  │                            │◄──────────────────────────────────│            │             │
  │                            │                                                │             │
  │                            │ validate(recommendations)                      │             │
  │                            │───────────────────────────────────────────────►│             │
  │                            │◄───────────────────────────────────────────────│             │
  │                            │                                                              │
  │                            │ build(telemetry)                                             │
  │                            │─────────────────────────────────────────────────────────────►│
  │                            │◄─────────────────────────────────────────────────────────────│
  │  return recommendations    │                                                              │
  │◄───────────────────────────│                                                              │
```
