# Recommendation Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│             domain/recommendation/ (Framework)               │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │      engine.py          │    │      registry.py        │  │
│  │  RecommendationEngine   │───►│  RecommendationRegistry │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │      models.py          │    │  providers/base.py      │  │
│  │  Recommendation DTOs    │    │  BaseRecProvider ABC    │  │
│  └─────────────────────────┘    └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
          │ depends on
          ▼
┌──────────────────────────────────────────────────────────────┐
│                 upstream/ matching & scoring                 │
│  MatchCollection  ScoreResult  ExplainabilityResult          │
└──────────────────────────────────────────────────────────────┘
```
