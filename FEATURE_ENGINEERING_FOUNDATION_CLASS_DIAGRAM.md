# Feature Engineering Foundation Class Diagram

## Book 04 — Feature Engineering | Milestone 4.1

The UML class diagram below details the structural mappings, dependencies, and relations in the Feature Engineering Foundation package:

```mermaid
classDiagram
    class FeatureExtractor {
        <<interface>>
        +extract(canonical_entities, context) Sequence~Feature~
    }

    class FeatureExtractorRegistry {
        -_registry: dict
        -_lock: Lock
        +register(extractor_type, extractor_cls)
        +get(extractor_type) Type~FeatureExtractor~
        +is_registered(extractor_type) bool
    }

    class FeatureExtractorFactory {
        -_registry: FeatureExtractorRegistry
        +get_extractor(extractor_type) FeatureExtractor
    }

    class FeatureEngineeringPipeline {
        -_logger: Logger
        +execute(canonical_entities, extractors, context) FeatureCollection
    }

    class FeatureEngineeringService {
        -_registry: FeatureExtractorRegistry
        -_factory: FeatureExtractorFactory
        -_pipeline: FeatureEngineeringPipeline
        -_logger: Logger
        +extract_features(canonical_entities, enabled_extractors, rules) FeatureCollection
    }

    class Feature {
        +feature_id: str
        +name: str
        +category: str
        +value: Any
        +confidence: float
        +locations: tuple
        +provenance: FeatureProvenance
        +metadata: FeatureMetadata
    }

    class FeatureProvenance {
        +source_entity_id: str
        +source_entity_type: str
        +source_section: str
        +source_document: str
        +matched_rules: tuple
    }

    class FeatureMetadata {
        +creation_timestamp: str
        +extractor_name: str
        +version: str
        +custom_attributes: Mapping
    }

    class FeatureCollection {
        +features: tuple
        +statistics: FeatureEngineeringStatistics
        +context: FeatureExtractionContext
    }

    FeatureExtractorRegistry ..> FeatureExtractor : maps classes
    FeatureExtractorFactory --> FeatureExtractorRegistry : resolves keys
    FeatureExtractorFactory ..> FeatureExtractor : instantiates
    FeatureEngineeringPipeline ..> FeatureExtractor : executes
    FeatureEngineeringService --> FeatureExtractorRegistry
    FeatureEngineeringService --> FeatureExtractorFactory
    FeatureEngineeringService --> FeatureEngineeringPipeline
    FeatureCollection *-- Feature
    Feature *-- FeatureProvenance
    Feature *-- FeatureMetadata
```
