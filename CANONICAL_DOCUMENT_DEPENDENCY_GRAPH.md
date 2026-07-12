# Canonical Document Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.4 — Canonical Document Validation  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the validation layer.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.document_processing]
        DVS[validation_service]
        DIV[integrity_validator]
        DCV[consistency_validator]
        DSB[statistics_builder]
        CDA[canonical_assembler]
        CDB[canonical_builder]
        models[canonical_models]
        rules[canonical_rules]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    DVS --> DIV
    DVS --> DCV
    DVS --> DSB
    DVS --> CDB
    DVS --> CDA
    DVS --> rules
    models --> Pydantic
    rules --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class DVS safe;
    class Pydantic external;
```
