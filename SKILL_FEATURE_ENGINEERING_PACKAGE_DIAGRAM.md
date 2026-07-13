# Skill Feature Engineering Package Diagram

## Book 04 — Feature Engineering | Milestone 4.2

The package boundary view details the files organized inside the `skills` sub-directory:

```mermaid
graph TD
    subgraph "domain.feature_engineering.skills"
        Extractor["extractor.py<br/>(SkillFeatureExtractor)"]
        Validator["validator.py<br/>(SkillFeatureValidator)"]
        Normalizer["normalizer.py<br/>(SkillFeatureNormalizer)"]
        Builder["builder.py<br/>(SkillFeatureBuilder)"]
        Stats["stats_builder.py<br/>(SkillFeatureStatisticsBuilder)"]
        Rules["rules.py<br/>(SkillFeatureRules)"]
    end

    subgraph "domain.feature_engineering"
        BaseExtractor["extractor.py<br/>(FeatureExtractor)"]
        BaseModels["models.py<br/>(Feature models)"]
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
