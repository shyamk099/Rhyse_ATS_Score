# Education Feature Engineering Package Diagram

## Book 04 — Feature Engineering | Milestone 4.4

The package boundary view details the files organized inside the `education` sub-directory:

```mermaid
graph TD
    subgraph "domain.feature_engineering.education"
        Extractor["extractor.py<br/>(EducationFeatureExtractor)"]
        Validator["validator.py<br/>(EducationFeatureValidator)"]
        Normalizer["normalizer.py<br/>(EducationFeatureNormalizer)"]
        Builder["builder.py<br/>(EducationFeatureBuilder)"]
        Stats["stats_builder.py<br/>(EducationFeatureStatisticsBuilder)"]
        Rules["rules.py<br/>(EducationFeatureRules)"]
    end

    subgraph "domain.feature_engineering"
        BaseExtractor["extractor.py<br/>(FeatureExtractor)"]
        BaseModels["models.py<br/>(Feature models / FeatureCategory)"]
    end

    Extractor --> BaseExtractor
    Extractor --> Validator
    Extractor --> Normalizer
    Extractor --> Builder
    Extractor --> Stats
    Extractor --> Rules

    Builder --> BaseModels
    Validator --> Rules
    Normalizer --> Rules
```
