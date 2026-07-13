# Experience Feature Engineering Class Diagram

## Book 04 — Feature Engineering | Milestone 4.3

The class diagram outlines the interfaces and helper classes supporting `ExperienceFeatureExtractor`:

```mermaid
classDiagram
    class FeatureExtractor {
        <<interface>>
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class ExperienceFeatureExtractor {
        -_logger: Logger
        -_validator: ExperienceFeatureValidator
        -_normalizer: ExperienceFeatureNormalizer
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class ExperienceFeatureValidator {
        -_logger: Logger
        +validate(entity, rules) list~str~
    }

    class ExperienceFeatureNormalizer {
        +normalize_text(text) str
        +normalize(entity, rules) ExperienceEntity
    }

    class ExperienceFeatureBuilder {
        +build(entity, correlation_id) Feature
    }

    class ExperienceFeatureStatisticsBuilder {
        +calculate(input_count, output_count, warnings_count, current_count) dict
    }

    class ExperienceFeatureRules {
        +enabled: bool
        +normalize_whitespace: bool
        +required_fields: Sequence
        +confidence_threshold: float
    }

    FeatureExtractor <|-- ExperienceFeatureExtractor
    ExperienceFeatureExtractor --> ExperienceFeatureValidator
    ExperienceFeatureExtractor --> ExperienceFeatureNormalizer
    ExperienceFeatureExtractor --> ExperienceFeatureBuilder
    ExperienceFeatureExtractor --> ExperienceFeatureStatisticsBuilder
    ExperienceFeatureExtractor ..> ExperienceFeatureRules
```
