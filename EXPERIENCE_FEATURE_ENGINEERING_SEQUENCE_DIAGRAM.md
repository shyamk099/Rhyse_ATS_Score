# Experience Feature Engineering Sequence Diagram

## Book 04 — Feature Engineering | Milestone 4.3

The timeline sequence below depicts the execution flow during experience feature extraction:

```mermaid
sequenceDiagram
    autonumber
    participant Pipeline as FeatureEngineeringPipeline
    participant Extractor as ExperienceFeatureExtractor
    participant Validator as ExperienceFeatureValidator
    participant Normalizer as ExperienceFeatureNormalizer
    participant Builder as ExperienceFeatureBuilder
    participant Stats as ExperienceFeatureStatisticsBuilder

    Pipeline ->> Extractor: extract(entities, context)
    Note over Extractor: Resolve ExperienceFeatureRules from config
    
    loop For each ExperienceEntity in experiences.entities
        Extractor ->> Validator: validate(entity, rules)
        Validator -->> Extractor: warnings_list
        Extractor ->> Normalizer: normalize(entity, rules)
        Normalizer -->> Extractor: normalized_entity
        Extractor ->> Builder: build(normalized_entity, corr_id)
        Note over Builder: Map 1:1 to Feature with generic value dict
        Builder -->> Extractor: Feature DTO
    end

    Extractor ->> Stats: calculate(input, output, warnings, current)
    Stats -->> Extractor: stats_dict
    
    Note over Extractor: Log telemetry stats
    Extractor -->> Pipeline: Sequence[Feature]
```
