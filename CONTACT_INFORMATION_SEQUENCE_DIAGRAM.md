# Contact Information Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.2 — Contact Information Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing contact information extraction.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant CIE as ContactInformationExtractor
    participant PCB as PatternCandidateBuilder
    participant CV as CandidateValidator
    participant CN as ContactNormalizer
    participant CEB as ContactEntityBuilder

    Client->>CIE: extract(segment, context)
    CIE->>PCB: find_candidates(segment.text_content, rules)
    PCB->>PCB: Scan email, phone, links patterns
    PCB-->>CIE: candidates list (ContactCandidate)
    
    loop For each candidate in candidates
        CIE->>CV: validate_candidate(candidate)
        alt is valid
            CIE->>CN: normalize(value, type)
            CN-->>CIE: normalized_value
            CIE->>CEB: build(candidate, normalized_value, segment_id, rules)
            CEB->>CEB: Map deterministic confidence
            CEB-->>CIE: ExtractedEntity
        end
    end
    
    CIE-->>Client: list[ExtractedEntity]
```
