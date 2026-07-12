# Section Detection Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.3 — Document Section Detection  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the section detection module.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.entity_extraction.section]
        SDS[service]
        SDP[pipeline]
        SCB[section_candidate_builder]
        HV[heading_validator]
        SBR[section_boundary_resolver]
        SB[section_builder]
        rules[section_rules]
        models[section_models]
    end

    subgraph Book02 [ats_engine.domain.document_processing]
        CD[canonical_models]
        seg[segmentation_models]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    SDS --> SDP
    SDP --> SCB
    SDP --> HV
    SDP --> SBR
    SDP --> SB
    SDP --> rules
    models --> seg
    models --> Pydantic
    rules --> Pydantic
    SCB --> CD

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class SDS safe;
    class Pydantic external;
```
