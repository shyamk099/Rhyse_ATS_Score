# Recommendation Class Diagram

```
┌──────────────────────────────────────────────┐
│             RecommendationEngine             │
├──────────────────────────────────────────────┤
│ - _registry: RecommendationRegistry          │
│ - _logger: Logger                            │
├──────────────────────────────────────────────┤
│ + recommend(match, score, exp) → RecResult   │
│ + registry: RecommendationRegistry           │
└──────────────────────────────────────────────┘
           │ uses
           ▼
┌──────────────────────────────────────────────┐
│            RecommendationRegistry            │
├──────────────────────────────────────────────┤
│ - _providers: dict                           │
├──────────────────────────────────────────────┤
│ + register(BaseRecommendationProvider)       │
│ + get(name) → BaseRecommendationProvider     │
│ + get_ordered_providers() → tuple            │
└──────────────────────────────────────────────┘
           │ manages
           ▼
┌──────────────────────────────────────────────┐
│          BaseRecommendationProvider (ABC)     │
├──────────────────────────────────────────────┤
│ + provider_name() → str                      │
│ + priority() → int                           │
│ + validate(match, score, exp)                │
│ + generate(match, score, exp) → tuple[Rec]   │
└──────────────────────────────────────────────┘
           │ produces
           ▼
┌──────────────────────────────────────────────┐
│                Recommendation                │
├──────────────────────────────────────────────┤
│ + recommendation_id: str                     │
│ + section: str                               │
│ + category: str                              │
│ + priority: int                              │
│ + title: str                                 │
│ + description: str                           │
│ + impact: float                              │
│ + metadata: dict                             │
└──────────────────────────────────────────────┘
```
