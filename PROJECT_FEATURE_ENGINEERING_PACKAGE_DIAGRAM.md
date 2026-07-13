# Project Feature Engineering Package Diagram

## Book 04 — Feature Engineering | Milestone 4.5

The package boundary view details the files organized inside the `project` sub-directory:

```mermaid
graph TD
    subgraph "domain.feature_engineering.project"
        Extractor["extractor.py<br/>(ProjectFeatureExtractor)"]
        Validator["validator.py<br/>(ProjectFeatureValidator)"]
        Normalizer["normalizer.py<br/>(ProjectFeatureNormalizer)"]
        Builder["builder.py<br/>(ProjectFeatureBuilder)"]
        Stats["stats_builder.py<br/>(ProjectFeatureStatisticsBuilder)"]
        Rules["rules.py<br/>(ProjectFeatureRules)"]
    end

    subgraph "domain.feature_engineering.common"
        CommonNorm["normalization.py"]
        CommonVal["validation.py"]
        CommonProv["provenance.py"]
        CommonUrl["url_mapping.py"]
    end

    Extractor --> Validator
    Extractor --> Normalizer
    Extractor --> Builder
    Extractor --> Stats
    Extractor --> Rules

    Normalizer --> CommonNorm
    Validator --> CommonVal
    Builder --> CommonProv
    Builder --> CommonUrl
```
