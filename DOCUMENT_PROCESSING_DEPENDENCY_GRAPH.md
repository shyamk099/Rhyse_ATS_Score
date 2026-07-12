# Document Processing Dependency Graph

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.1 — Document Processing Foundation  
**Status:** COMPLETE  

---

# Purpose

This document outlines compile-time and runtime dependency vectors of the Document Processing Foundation.

---

# Dependency Graph

```mermaid
flowchart TD
    subgraph Core [ats_engine.domain.document_processing]
        DPP[document_processing package]
    end

    subgraph Logging [ats_engine.infrastructure.logging]
        LoggingPackage[logging package]
    end

    subgraph External [External Third Party]
        PyMuPDF[PyMuPDF]
        docx[python-docx]
        Pydantic[Pydantic v2]
    end

    DPP --> Logging
    DPP --> PyMuPDF
    DPP --> docx
    DPP --> Pydantic

    %% Validation constraints
    classDef safe stroke:#33cc33,stroke-width:2px;
    classDef external stroke:#333,stroke-dasharray: 5 5;
    class DPP safe;
    class PyMuPDF,docx,Pydantic external;
```
