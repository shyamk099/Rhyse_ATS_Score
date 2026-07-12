# Document Segmentation Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.3 — Document Segmentation & Reading Order  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the physical segmentation layer.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.document_processing]
        DS[segmenter]
        ROR[reading_order]
        PSB[segment_builder]
        SV[segment_validator]
        SM[segmentation_models]
        rules[segmentation_rules]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    DS --> ROR
    DS --> PSB
    DS --> SV
    DS --> SM
    DS --> rules
    SM --> Pydantic
    rules --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class DS safe;
    class Pydantic external;
```
