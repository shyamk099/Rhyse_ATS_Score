# Structural Analysis Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.2 — Resume & JD Structural Analysis  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram for the structural analyzer layer.

---

# Components

```mermaid
flowchart TD
    subgraph Subsystem [Document Processing Subsystem]
        SA[Structural Analyzer]
        SAR[Structural Analysis Rules]
        models[Structure Pydantic Models]
    end

    Client[Engine Pipeline Coordinator] -->|Passes raw/norm docs| SA
    SA -->|Validates config with| SAR
    SA -->|Instantiates| models
```
