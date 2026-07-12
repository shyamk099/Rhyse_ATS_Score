# Section Detection Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.3 — Document Section Detection  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing document section detection.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant SDS as SectionDetectionService
    participant SCB as SectionCandidateBuilder
    participant HV as HeadingValidator
    participant SBR as SectionBoundaryResolver
    participant SB as SectionBuilder
    participant SC as SectionCollection

    Client->>SDS: detect_sections(doc, config)
    SDS->>SCB: find_candidates(doc, rules)
    SCB->>SCB: Check physical layout and aliases
    SCB-->>SDS: candidates list (SectionCandidate)
    
    loop For each candidate in candidates
        SDS->>HV: validate(candidate, rules)
        HV-->>SDS: is_valid (bool)
    end
    
    SDS->>SBR: resolve_boundaries(doc, validated_candidates)
    SBR->>SBR: Scan segments sequentially
    SBR-->>SDS: boundaries list (SectionBoundary)
    
    loop For each boundary in boundaries
        SDS->>SB: build_section(boundary, segments, rules)
        SB->>SB: Calculate lines, page ranges & reasons
        SB-->>SDS: Section
    end
    
    SDS->>SC: Instantiate(sections, stats)
    SC-->>SDS: SectionCollection
    SDS-->>Client: SectionCollection
```
