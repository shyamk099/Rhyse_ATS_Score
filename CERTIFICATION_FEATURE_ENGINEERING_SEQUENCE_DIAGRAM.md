# Certification Feature Engineering Sequence Diagram

## Book 04 — Feature Engineering | Milestone 4.5

The timeline sequence below depicts the execution flow during certification feature extraction:

```mermaid
sequenceDiagram
    autonumber
    participant Pipeline as FeatureEngineeringPipeline
    participant Extractor as CertificationFeatureExtractor
    participant Validator as CertificationFeatureValidator
    participant Normalizer as CertificationFeatureNormalizer
    participant Builder as CertificationFeatureBuilder
    participant Stats as CertificationFeatureStatisticsBuilder

    Pipeline ->> Extractor: extract(entities, context)
    Note over Extractor: Resolve CertificationFeatureRules from config
    
    loop For each CertificationEntity in certifications.entities
        Extractor ->> Validator: validate(entity, rules)
        Validator -->> Extractor: warnings_list
        Extractor ->> Normalizer: normalize(entity, rules)
        Normalizer -->> Extractor: normalized_entity
        Extractor ->> Builder: build(normalized_entity, corr_id)
        Note over Builder: Map 1:1 to Feature with generic value dict
        Builder -->> Extractor: Feature DTO
    end

    Extractor ->> Stats: calculate(input, output, warnings, active_count)
    Stats -->> Extractor: stats_dict
    
    Note over Extractor: Log telemetry stats
    Extractor -->> Pipeline: Sequence[Feature]
```
