# Document Processing Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.1 — Document Processing Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram representing the Document Processing Foundation layer.

---

# Architecture

```mermaid
classDiagram
    class DocumentProcessingService {
        -_factory: DocumentParserFactory
        -_logger: Logger
        +parse(file_path: Path) ParsingResult
    }

    class DocumentParserFactory {
        -_registry: DocumentParserRegistry
        +get_parser(file_path: Path) DocumentParser
        -_detect_format_by_signature(header: bytes) str
    }

    class DocumentParserRegistry {
        -_registry: dict
        +register(format_key: str, parser_cls: Type) None
        +get(format_key: str) Type
    }

    class DocumentParser {
        <<interface>>
        +parse(file_path: Path) RawDocument
    }

    class PdfDocumentParser {
        +parse(file_path: Path) RawDocument
    }

    class DocxDocumentParser {
        +parse(file_path: Path) RawDocument
    }

    class TextNormalizer {
        +normalize(text: str) str
        +normalize_line_endings(text: str) str
        +normalize_unicode(text: str) str
        +cleanup_control_characters(text: str) str
        +cleanup_hyphens(text: str) str
        +normalize_whitespaces(text: str) str
        +normalize_empty_lines(text: str) str
    }

    class RawDocument {
        +filename: str
        +file_size_bytes: int
        +raw_content: str
        +pages: tuple
    }

    class NormalizedDocument {
        +cleaned_content: str
        +paragraph_count: int
        +line_count: int
        +char_count: int
    }

    class DocumentMetadata {
        +file_size_bytes: int
        +page_count: int
        +character_count: int
        +line_count: int
        +paragraph_count: int
        +extraction_duration_seconds: float
        +parser_used: str
        +encoding: str
    }

    class ParsingResult {
        +raw_document: RawDocument
        +normalized_document: NormalizedDocument
        +metadata: DocumentMetadata
    }

    DocumentParser <|.. PdfDocumentParser
    DocumentParser <|.. DocxDocumentParser
    DocumentProcessingService --> DocumentParserFactory : uses
    DocumentParserFactory --> DocumentParserRegistry : uses
    DocumentProcessingService ..> TextNormalizer : uses
    DocumentProcessingService ..> ParsingResult : compiles
    ParsingResult --> RawDocument
    ParsingResult --> NormalizedDocument
    ParsingResult --> DocumentMetadata
```
