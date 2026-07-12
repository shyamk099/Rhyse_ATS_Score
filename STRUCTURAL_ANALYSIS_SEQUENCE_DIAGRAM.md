# Structural Analysis Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.2 — Resume & JD Structural Analysis  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing structural analysis.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant SA as StructuralAnalyzer
    participant Rules as StructuralAnalysisRules
    participant DL as DocumentLayout

    Client->>SA: analyze(raw_doc, norm_doc)
    SA->>Rules: Query heuristics (symbols, lengths)
    Rules-->>SA: Heuristic parameters
    loop For each page in raw_doc
        loop For each line in page
            SA->>SA: Classify (Heading/List/Table/Text)
        end
    end
    SA->>SA: Group matching line sequences into PhysicalBlocks
    SA->>DL: Instantiate(blocks)
    DL-->>SA: DocumentLayout (immutable)
    SA-->>Client: DocumentLayout
```
