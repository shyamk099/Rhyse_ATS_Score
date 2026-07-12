# Section Detection Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.3 — Document Section Detection  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram for the section detection subsystem.

---

# Components

```mermaid
flowchart TD
    subgraph Subsystem [Section Detection Subsystem]
        SDS[Section Detection Service]
        SDP[Section Detection Pipeline]
        SCB[Section Candidate Builder]
        HV[Heading Validator]
        SBR[Section Boundary Resolver]
        SB[Section Builder]
        rules[Section Detection Rules]
    end

    Client[ATS Parser Pipeline] -->|Call| SDS
    SDS --> SDP
    SDP --> SCB
    SDP --> HV
    SDP --> SBR
    SDP --> SB
    SDP --> rules
```
