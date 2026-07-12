# Contact Information Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.2 — Contact Information Extraction  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the contact extraction module.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.entity_extraction.contact]
        CIE[extractor]
        PCB[pattern_candidate_builder]
        CV[candidate_validator]
        CN[normalizer]
        CEB[entity_builder]
        rules[contact_rules]
        cand[contact_candidate]
    end

    subgraph Foundation [ats_engine.domain.entity_extraction]
        EE[extractor interface]
        context[models context]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    CIE --> EE
    CIE --> context
    CIE --> PCB
    CIE --> CV
    CIE --> CN
    CIE --> CEB
    CIE --> rules
    PCB --> cand
    rules --> Pydantic
    cand --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class CIE safe;
    class Pydantic external;
```
