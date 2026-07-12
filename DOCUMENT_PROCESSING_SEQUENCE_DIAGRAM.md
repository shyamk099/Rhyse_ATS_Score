# Document Processing Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.1 — Document Processing Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing the Document Processing execution path.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Service as DocumentProcessingService
    participant Factory as DocumentParserFactory
    participant Registry as DocumentParserRegistry
    participant Parser as DocumentParser
    participant Normalizer as TextNormalizer

    Client->>Service: parse(file_path)
    Service->>Factory: get_parser(file_path)
    Factory->>Factory: Read file signature (magic bytes)
    Factory->>Registry: get(detected_format)
    Registry-->>Factory: ParserClass reference
    Factory-->>Service: ParserInstance (stateless)

    Service->>Parser: parse(file_path)
    Parser->>Parser: Extract text (PDF pages / DOCX paragraphs)
    Parser-->>Service: RawDocument

    Service->>Normalizer: normalize(raw_content)
    Normalizer->>Normalizer: unicode form, spaces, empty lines, hyphens
    Normalizer-->>Service: cleaned_text

    Service->>Service: Calculate stats (line, character, paragraph counts)
    Service-->>Client: ParsingResult
```
