# Section Detection Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.3 — Document Section Detection  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the section detection module.

---

# Architecture

```mermaid
classDiagram
    class SectionDetectionService {
        -_logger: Logger
        +detect_sections(document: CanonicalDocument, rule_engine_config: Mapping) SectionCollection
    }

    class SectionCandidateBuilder {
        +find_candidates(document: CanonicalDocument, rules: SectionDetectionRules) Sequence~SectionCandidate~
    }

    class HeadingValidator {
        +validate(candidate: SectionCandidate, rules: SectionDetectionRules) bool
    }

    class SectionBoundaryResolver {
        +resolve_boundaries(document: CanonicalDocument, validated_candidates: Sequence~SectionCandidate~) Sequence~SectionBoundary~
    }

    class SectionBuilder {
        +build_section(boundary: SectionBoundary, segments: Sequence~DocumentSegment~, rules: SectionDetectionRules) Section
    }

    class SectionDetectionRules {
        +section_aliases: Mapping
        +heading_confidence_default: float
        +heading_confidence_alias_match: float
        +max_heading_words: int
    }

    class SectionCandidate {
        +block_index: int
        +matched_text: str
        +section_type: str
        +confidence: float
        +confidence_reason: str
    }

    class SectionMetadata {
        +section_type: str
        +page_range: tuple~int_int~
        +start_line: int
        +end_line: int
        +confidence: float
        +confidence_reason: str
    }

    class Section {
        +section_type: str
        +text_content: str
        +metadata: SectionMetadata
        +associated_segments: tuple~DocumentSegment~
    }

    class SectionCollection {
        +sections: tuple~Section~
        +statistics: SectionDetectionStatistics
    }

    SectionDetectionService --> SectionDetectionRules : consumes
    SectionDetectionService ..> SectionCollection : compiles
    SectionCandidateBuilder ..> SectionCandidate : compiles
    SectionBoundaryResolver ..> SectionBoundary : compiles
    SectionBuilder ..> Section : compiles
    Section --> SectionMetadata : has
    SectionCollection --> Section : aggregates
```
