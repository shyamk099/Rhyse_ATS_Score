# Document Segmentation Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.3 — Document Segmentation & Reading Order  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the document segmentation layer.

---

# Architecture

```mermaid
classDiagram
    class DocumentSegmenter {
        -_rules: SegmentationRules
        -_logger: Logger
        +segment(layout: DocumentLayout) SegmentCollection
    }

    class ReadingOrderResolver {
        +resolve(layout: DocumentLayout) Sequence~PhysicalBlock~
    }

    class PhysicalSegmentBuilder {
        +build_segments(blocks: Sequence~PhysicalBlock~, rules: SegmentationRules) list~DocumentSegment~
    }

    class SegmentValidator {
        +validate(layout: DocumentLayout, segments: Sequence~DocumentSegment~) None
        -_get_block_key(block: PhysicalBlock) str
    }

    class SegmentationRules {
        +max_segment_characters: int
        +max_segment_blocks: int
        +split_on_page_transition: bool
    }

    class SegmentMetadata {
        +segment_id: str
        +reading_order: int
        +page_range: tuple~int_int~
        +block_range: tuple~int_int~
        +character_count: int
        +line_count: int
    }

    class DocumentSegment {
        +segment_id: str
        +text_content: str
        +metadata: SegmentMetadata
        +associated_blocks: tuple~PhysicalBlock~
    }

    class SegmentCollection {
        +segments: tuple~DocumentSegment~
        +total_segments: int
        +total_characters: int
    }

    DocumentSegmenter --> ReadingOrderResolver : uses
    DocumentSegmenter --> PhysicalSegmentBuilder : uses
    DocumentSegmenter --> SegmentValidator : uses
    DocumentSegmenter --> SegmentationRules : consumes
    DocumentSegmenter ..> SegmentCollection : compiles
    SegmentCollection --> DocumentSegment : aggregates
    DocumentSegment --> SegmentMetadata : has
```
