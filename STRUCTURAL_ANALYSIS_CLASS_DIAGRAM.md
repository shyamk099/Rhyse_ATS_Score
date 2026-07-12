# Structural Analysis Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.2 — Resume & JD Structural Analysis  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the layout analysis layer.

---

# Architecture

```mermaid
classDiagram
    class StructuralAnalyzer {
        -_rules: StructuralAnalysisRules
        -_numbered_regexes: list
        +analyze(raw_document: RawDocument, normalized_document: NormalizedDocument) DocumentLayout
        -_group_lines_into_blocks(lines: list~PhysicalLine~) list~PhysicalBlock~
        -_classify_line(line: PhysicalLine) BlockType
        -_compile_block(block_type: BlockType, lines: list~PhysicalLine~) PhysicalBlock
    }

    class StructuralAnalysisRules {
        +max_heading_length: int
        +bullet_symbols: tuple
        +numbered_patterns: tuple
        +heading_all_caps: bool
        +table_min_delimiters: int
        +table_delimiters: tuple
    }

    class BlockType {
        <<enum>>
        TEXT
        HEADING
        LIST
        TABLE
        UNKNOWN
    }

    class PhysicalLine {
        +text: str
        +line_number: int
        +page_number: int
        +indentation_spaces: int
        +character_count: int
    }

    class PhysicalBlock {
        +block_type: BlockType
        +lines: tuple~PhysicalLine~
        +raw_text: str
    }

    class DocumentLayout {
        +blocks: tuple~PhysicalBlock~
        +total_blocks: int
        +total_lines: int
    }

    StructuralAnalyzer --> StructuralAnalysisRules : consumes
    StructuralAnalyzer ..> DocumentLayout : compiles
    DocumentLayout --> PhysicalBlock : aggregates
    PhysicalBlock --> PhysicalLine : aggregates
    PhysicalBlock --> BlockType : typed by
```
