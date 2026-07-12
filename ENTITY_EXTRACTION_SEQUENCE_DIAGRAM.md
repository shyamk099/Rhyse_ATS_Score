# Entity Extraction Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.1 — Entity Extraction Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing entity extraction execution.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Service as EntityExtractionService
    participant Pipeline as EntityExtractionPipeline
    participant Factory as EntityExtractorFactory
    participant Registry as EntityExtractorRegistry
    participant Extractor as EntityExtractor
    participant Collection as EntityCollection

    Client->>Service: extract(doc, types, config, corr_id)
    Service->>Service: Setup tracking correlation ID
    Service->>Pipeline: execute(context, types)
    
    loop For each type in types
        Pipeline->>Factory: get_extractor(type)
        Factory->>Registry: get(type)
        Registry-->>Factory: ExtractorClass reference
        Factory-->>Pipeline: ExtractorInstance (stateless)
        
        loop For each segment in doc
            Pipeline->>Extractor: extract(segment, context)
            Extractor->>Extractor: Run generic segment text parser
            Extractor-->>Pipeline: list[ExtractedEntity]
        end
    end
    
    Pipeline->>Collection: Instantiate(entities, stats)
    Collection-->>Pipeline: EntityCollection (immutable)
    Pipeline-->>Service: EntityCollection
    Service-->>Client: EntityCollection
```
