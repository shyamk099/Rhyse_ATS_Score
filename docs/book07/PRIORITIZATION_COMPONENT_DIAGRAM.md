# Prioritization Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│          domain/recommendation/prioritization/               │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ prioritization_engine.py│───►│ prioritization_rules.py │  │
│  │ PrioritizationEngine    │    │ PrioritizationRules     │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ prioritization_builder.py│   │ prioritization_valid... │  │
│  │ PrioritizationBuilder   │    │ PrioritizationValidator │  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ prioritization_stats... │                                 │
│  │ PrioritizationStatistics│                                 │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
