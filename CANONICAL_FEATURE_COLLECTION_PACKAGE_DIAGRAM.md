# Canonical Feature Collection Package Diagram

## Book 04 — Feature Engineering | Milestone 4.6

The package boundary view details the files organized inside the `canonical` feature engineering sub-directory:

```mermaid
graph TD
    subgraph "domain.feature_engineering.canonical"
        Service["service.py<br/>(CanonicalFeatureCollectionService)"]
        Pipeline["pipeline.py<br/>(CanonicalFeatureCollectionPipeline)"]
        Validator["validator.py<br/>(FeatureValidator)"]
        Resolver["duplicate_resolver.py<br/>(DuplicateFeatureResolver)"]
        Cross["cross_validator.py<br/>(CrossFeatureValidator)"]
        Stats["stats_builder.py<br/>(FeatureStatisticsBuilder)"]
        Summary["validation_summary_builder.py<br/>(ValidationSummaryBuilder)"]
        Builder["builder.py<br/>(CanonicalFeatureCollectionBuilder)"]
        Rules["rules.py<br/>(CanonicalFeatureValidationRules)"]
    end

    subgraph "domain.feature_engineering"
        BaseModels["models.py<br/>(ValidationErrorDetail, ValidationWarningDetail, ValidationSummary, FeatureStatistics, CanonicalFeatureCollection)"]
        Exceptions["exceptions.py<br/>(FeatureValidationError, DuplicateFeatureError, CrossFeatureValidationError, CanonicalCollectionBuildError)"]
    end

    Service --> Pipeline
    Pipeline --> Validator
    Pipeline --> Resolver
    Pipeline --> Cross
    Pipeline --> Stats
    Pipeline --> Summary
    Pipeline --> Builder
    Pipeline --> Rules

    Builder --> BaseModels
    Pipeline --> Exceptions
```
