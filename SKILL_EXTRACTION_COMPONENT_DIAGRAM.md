# Skill Extraction Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.4 — Skill Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram for the skill extraction subsystem.

---

# Components

```mermaid
flowchart TD
    subgraph Subsystem [Skill Extraction Subsystem]
        SES[Skill Extraction Service]
        SEP[Skill Extraction Pipeline]
        SCB[Skill Candidate Builder]
        SCV[Skill Candidate Validator]
        SN[Skill Normalizer]
        DR[Duplicate Resolver]
        SEB[Skill Entity Builder]
        rules[Skill Extraction Rules]
    end

    subgraph ExtensibilityPoints [Extensible Interfaces]
        SM[SkillMatcher Interface]
        DM[DictionaryMatcher]
    end

    Client[ATS Processing Engine] -->|Call| SES
    SES --> SEP
    SEP --> SCB
    SCB -->|Uses| SM
    DM -.->|Implements| SM
    SEP --> SCV
    SEP --> SN
    SEP --> DR
    SEP --> SEB
    SEP --> rules
```
