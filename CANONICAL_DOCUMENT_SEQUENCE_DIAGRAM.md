# Canonical Document Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.4 — Canonical Document Validation  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing canonical document validation.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Service as DocumentValidationService
    participant Integrity as DocumentIntegrityValidator
    participant Consistency as DocumentConsistencyValidator
    participant StatsBuilder as DocumentStatisticsBuilder
    participant Builder as CanonicalDocumentBuilder
    participant Assembler as CanonicalDocumentAssembler

    Client->>Service: validate_and_assemble(raw_doc, norm_doc, layout, segments, parser)
    
    Service->>Integrity: validate(layout, segments, rules)
    Integrity->>Integrity: check empty structures and page order
    Integrity-->>Service: integrity ok
    
    Service->>Consistency: validate(norm_doc, layout, segments, rules)
    Consistency->>Consistency: check block references and character count
    Consistency-->>Service: consistency ok
    
    Service->>StatsBuilder: build(norm_doc, layout, segments)
    StatsBuilder-->>Service: stats
    
    Service->>Builder: build_metadata(raw_doc, page_count, parser)
    Builder-->>Service: metadata
    
    Service->>Assembler: assemble(norm_doc, layout, segments, metadata, stats)
    Assembler-->>Service: CanonicalDocument
    
    Service-->>Client: CanonicalDocument
```
