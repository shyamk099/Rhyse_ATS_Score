# Structural Analysis Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.2 — Resume & JD Structural Analysis  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the structural analysis layer.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.document_processing]
        SA[structural_analyzer]
        SAR[structural_rules]
        SM[structure_models]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    SA --> SAR
    SA --> SM
    SAR --> Pydantic
    SM --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class SA safe;
    class Pydantic external;
```
