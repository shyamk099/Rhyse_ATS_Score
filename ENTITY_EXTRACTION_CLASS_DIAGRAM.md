# Entity Extraction Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.1 — Entity Extraction Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the entity extraction foundation layer.

---

# Architecture

```mermaid
classDiagram
    class EntityExtractionService {
        -_pipeline: EntityExtractionPipeline
        -_logger: Logger
        +extract(document: CanonicalDocument, extractor_types: Sequence~str~, rule_engine_config: Mapping, correlation_id: str) EntityCollection
    }

    class EntityExtractionPipeline {
        -_factory: EntityExtractorFactory
        +execute(context: EntityExtractionContext, extractor_types: Sequence~str~) EntityCollection
    }

    class EntityExtractorRegistry {
        -_registry: dict
        +register(extractor_type: str, extractor_cls: Type) None
        +get(extractor_type: str) Type
    }

    class EntityExtractorFactory {
        -_registry: EntityExtractorRegistry
        +get_extractor(extractor_type: str) EntityExtractor
    }

    class EntityExtractor {
        <<interface>>
        +extract(segment: DocumentSegment, context: EntityExtractionContext) Sequence~ExtractedEntity~
    }

    class EntityExtractionContext {
        +canonical_document: CanonicalDocument
        +correlation_id: str
        +rule_engine_config: Mapping
    }

    class EntityLocation {
        +segment_id: str
        +start_char: int
        +end_char: int
    }

    class ExtractedEntity {
        +entity_type: str
        +value: str
        +confidence: float
        +location: EntityLocation
        +metadata: Mapping
    }

    class EntityExtractionStatistics {
        +extractor_counts: Mapping
        +total_entities: int
        +execution_duration_seconds: float
    }

    class EntityCollection {
        +entities: tuple~ExtractedEntity~
        +statistics: EntityExtractionStatistics
    }

    EntityExtractionService --> EntityExtractionPipeline : uses
    EntityExtractionPipeline --> EntityExtractorFactory : uses
    EntityExtractorFactory --> EntityExtractorRegistry : uses
    EntityExtractionPipeline ..> EntityExtractor : executes
    EntityExtractionPipeline ..> EntityCollection : compiles
    EntityCollection --> ExtractedEntity : aggregates
    EntityCollection --> EntityExtractionStatistics : aggregates
    ExtractedEntity --> EntityLocation : aggregates
    EntityExtractionPipeline ..> EntityExtractionContext : consumes
```
