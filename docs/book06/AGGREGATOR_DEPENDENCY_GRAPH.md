# Explainability Dependency Graph

```
ExplainabilityEngine
    ├── SectionWeightConfiguration        (aggregation.weighting)
    ├── ExplainabilityFormatter           (explainability.formatter)
    ├── ExplainabilityMetadataBuilder     (explainability.metadata_builder)
    └── ExplainabilityStatisticsBuilder   (explainability.statistics_builder)

ScoringFactory
    └── create_default_explainer()
            ├── SectionWeightConfiguration
            └── ExplainabilityEngine(weight_config)

Exceptions (no circular deps):
    ScoringError
        └── ExplainabilityError
              ├── FormattingError             (raised by ExplainabilityFormatter)
              └── ExplainabilityValidationError (raised by ExplainabilityEngine)
```
