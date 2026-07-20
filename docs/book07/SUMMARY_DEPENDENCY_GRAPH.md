# Summary Dependency Graph

```mermaid
graph LR
    subgraph "Upstream (Read-Only)"
        RM["recommendation.models"]
        PM["prioritization.models"]
        PR["prioritization.prioritization_rules"]
        OM["orchestration.models"]
        BP["post_processors.base"]
        EX["exceptions"]
    end

    subgraph "Summary Package"
        SM["summary.models"]
        SP["summary.policy"]
        SB["summary.summary_builder"]
        SV["summary.summary_validator"]
        SS["summary.summary_statistics_builder"]
        SE["summary.summary_engine"]
    end

    SE --> BP
    SE --> PR
    SE --> SM
    SE --> SB
    SE --> SV
    SE --> SS
    SE -.-> OM

    SB --> SM
    SB --> SP
    SB --> OM
    SB --> PR
    SB --> RM

    SV --> SM
    SV --> OM
    SV --> EX

    SP --> SM

    SS --> SM
```

## Dependency Rules

1. `summary.*` depends on `orchestration.models` (input DTO) — read-only.
2. `summary.*` depends on `prioritization.prioritization_rules` (threshold classification) — read-only.
3. `summary.*` depends on `recommendation.models` (Recommendation DTO) — read-only.
4. No upstream package depends on `summary.*`.
5. Only `factory.py` imports `summary.summary_engine` for registration.
