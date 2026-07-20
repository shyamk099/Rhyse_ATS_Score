# Certification Provider Sequence Diagram

```
Engine            CertificationRecommendationProvider   Rules      Builder      Validator      Stats
  │                            │                       │           │            │             │
  │  generate(context)         │                       │           │            │             │
  │───────────────────────────►│                       │           │            │             │
  │                            │ evaluate_missing/match│           │            │             │
  │                            │──────────────────────►│           │            │             │
  │                            │◄──────────────────────│           │            │             │
  │                            │                                   │            │             │
  │                            │ build_missing/partial/expired()   │            │             │
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
