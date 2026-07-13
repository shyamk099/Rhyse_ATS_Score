# Education Feature Engineering Class Diagram

## Book 04 — Feature Engineering | Milestone 4.4

The class diagram outlines the interfaces and helper classes supporting `EducationFeatureExtractor`:

```mermaid
classDiagram
    class FeatureExtractor {
        <<interface>>
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class EducationFeatureExtractor {
        -_logger: Logger
        -_validator: EducationFeatureValidator
        -_normalizer: EducationFeatureNormalizer
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class EducationFeatureValidator {
        -_logger: Logger
        +validate(entity, rules) list~str~
    }

    class EducationFeatureNormalizer {
        +normalize_text(text) str
        +normalize(entity, rules) EducationEntity
    }

    class EducationFeatureBuilder {
        +build(entity, correlation_id) Feature
    }

    class EducationFeatureStatisticsBuilder {
        +calculate(input_count, output_count, warnings_count, degree_count) dict
    }

    class EducationFeatureRules {
        +enabled: bool
        +normalize_whitespace: bool
        +required_fields: Sequence
        +confidence_threshold: float
    }

    FeatureExtractor <|-- EducationFeatureExtractor
    EducationFeatureExtractor --> EducationFeatureValidator
    EducationFeatureExtractor --> EducationFeatureNormalizer
    EducationFeatureExtractor --> EducationFeatureBuilder
    EducationFeatureExtractor --> EducationFeatureStatisticsBuilder
    EducationFeatureExtractor ..> EducationFeatureRules
```
