# Document Segmentation Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.3 — Document Segmentation & Reading Order  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram for the segmentation pipeline.

---

# Components

```mermaid
flowchart TD
    subgraph Subsystem [Document Processing Subsystem]
        DS[Document Segmenter]
        ROR[Reading Order Resolver]
        PSB[Physical Segment Builder]
        SV[Segment Validator]
        rules[Segmentation Rules]
        models[Segmentation Pydantic Models]
    end

    Client[Pipeline Coordinator] -->|Passes layout| DS
    DS -->|Uses| ROR
    DS -->|Uses| PSB
    DS -->|Uses| SV
    DS -->|Consumes| rules
    DS -->|Instantiates| models
```
