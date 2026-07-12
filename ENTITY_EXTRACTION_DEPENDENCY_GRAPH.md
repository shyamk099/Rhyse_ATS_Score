# Entity Extraction Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.1 — Entity Extraction Foundation  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the entity extraction foundation layer.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.entity_extraction]
        EES[service]
        EEP[pipeline]
        EEF[factory]
        EER[registry]
        models[models]
    end

    subgraph Book02 [ats_engine.domain.document_processing]
        CD[canonical_models]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    EES --> EEP
    EEP --> EEF
    EEF --> EER
    EEP --> models
    models --> CD
    models --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class EES safe;
    class Pydantic external;
```
