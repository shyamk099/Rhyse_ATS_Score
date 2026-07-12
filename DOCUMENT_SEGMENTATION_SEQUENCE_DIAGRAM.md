# Document Segmentation Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.3 — Document Segmentation & Reading Order  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing document segmentation flow.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Segmenter as DocumentSegmenter
    participant Resolver as ReadingOrderResolver
    participant Builder as PhysicalSegmentBuilder
    participant Validator as SegmentValidator
    participant SC as SegmentCollection

    Client->>Segmenter: segment(layout)
    Segmenter->>Resolver: resolve(layout)
    Resolver->>Resolver: Sort blocks by page and line sequence
    Resolver-->>Segmenter: sorted blocks list

    Segmenter->>Builder: build_segments(sorted_blocks, rules)
    loop For each block
        Builder->>Builder: Check size limit / page transitions
        alt limit exceeded
            Builder->>Builder: Flush accumulated blocks to DocumentSegment
        end
    end
    Builder-->>Segmenter: built segments list

    Segmenter->>Validator: validate(layout, segments)
    Validator->>Validator: Audits counts, duplicates, page sequence
    Validator-->>Segmenter: validation success

    Segmenter->>SC: Instantiate(segments)
    SC-->>Segmenter: SegmentCollection (immutable)
    Segmenter-->>Client: SegmentCollection
```
