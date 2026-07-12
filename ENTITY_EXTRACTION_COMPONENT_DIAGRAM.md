# Entity Extraction Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.1 — Entity Extraction Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram for the extraction layer.

---

# Components

```mermaid
flowchart TD
    subgraph Subsystem [Entity Extraction Subsystem]
        EES[Entity Extraction Service]
        EEP[Entity Extraction Pipeline]
        EEF[Entity Extractor Factory]
        EER[Entity Extractor Registry]
        models[Extraction Pydantic Models]
    end

    subgraph InterfaceContracts [Extensibility Points]
        EE[EntityExtractor Protocol]
    end

    Client[ATS Scoring Pipeline] -->|Call| EES
    EES --> EEP
    EEP --> EEF
    EEF --> EER
    EEP -->|Executes| EE
    EEP -->|Instantiates| models
```
