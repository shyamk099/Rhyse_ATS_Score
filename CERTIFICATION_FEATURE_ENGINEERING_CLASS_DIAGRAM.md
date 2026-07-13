# Certification Feature Engineering Class Diagram

## Book 04 — Feature Engineering | Milestone 4.5

The class diagram outlines the interfaces and helper classes supporting `CertificationFeatureExtractor`:

```mermaid
classDiagram
    class FeatureExtractor {
        <<interface>>
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class CertificationFeatureExtractor {
        -_logger: Logger
        -_validator: CertificationFeatureValidator
        -_normalizer: CertificationFeatureNormalizer
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class CertificationFeatureValidator {
        -_logger: Logger
        +validate(entity, rules) list~str~
    }

    class CertificationFeatureNormalizer {
        +normalize(entity, rules) CertificationEntity
    }

    class CertificationFeatureBuilder {
        +build(entity, correlation_id) Feature
    }

    class CertificationFeatureStatisticsBuilder {
        +calculate(input_count, output_count, warnings_count, active_count) dict
    }

    class CertificationFeatureRules {
        +enabled: bool
        +normalize_whitespace: bool
        +required_fields: Sequence
        +confidence_threshold: float
    }

    FeatureExtractor <|-- CertificationFeatureExtractor
    CertificationFeatureExtractor --> CertificationFeatureValidator
    CertificationFeatureExtractor --> CertificationFeatureNormalizer
    CertificationFeatureExtractor --> CertificationFeatureBuilder
    CertificationFeatureExtractor --> CertificationFeatureStatisticsBuilder
    CertificationFeatureExtractor ..> CertificationFeatureRules
```
