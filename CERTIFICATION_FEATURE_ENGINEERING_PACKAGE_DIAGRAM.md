# Certification Feature Engineering Package Diagram

## Book 04 — Feature Engineering | Milestone 4.5

The package boundary view details the files organized inside the `certification` sub-directory:

```mermaid
graph TD
    subgraph "domain.feature_engineering.certification"
        Extractor["extractor.py<br/>(CertificationFeatureExtractor)"]
        Validator["validator.py<br/>(CertificationFeatureValidator)"]
        Normalizer["normalizer.py<br/>(CertificationFeatureNormalizer)"]
        Builder["builder.py<br/>(CertificationFeatureBuilder)"]
        Stats["stats_builder.py<br/>(CertificationFeatureStatisticsBuilder)"]
        Rules["rules.py<br/>(CertificationFeatureRules)"]
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
