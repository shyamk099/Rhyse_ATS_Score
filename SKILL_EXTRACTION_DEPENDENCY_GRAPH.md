# Skill Extraction Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.4 — Skill Extraction  
**Status:** COMPLETE  

---

# Purpose

This document details the dependencies of the skill extraction module.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.entity_extraction.skills]
        SES[service]
        SEP[pipeline]
        SCB[skill_candidate_builder]
        SCV[skill_candidate_validator]
        SN[skill_normalizer]
        DR[duplicate_resolver]
        SEB[skill_entity_builder]
        rules[skill_rules]
        models[skill_models]
        SM[matcher interface]
    end

    subgraph Book03Section [ats_engine.domain.entity_extraction.section]
        sec_models[section_models]
    end

    subgraph Book02 [ats_engine.domain.document_processing]
        CD[canonical_models]
    end

    subgraph External [External Third Party]
        Pydantic[Pydantic v2]
    end

    SES --> SEP
    SEP --> SCB
    SEP --> SCV
    SEP --> SN
    SEP --> DR
    SEP --> SEB
    SEP --> rules
    SCB --> SM
    SCB --> sec_models
    SCB --> CD
    models --> Pydantic
    rules --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class SES safe;
    class Pydantic external;
```
