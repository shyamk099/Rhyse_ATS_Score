# Document Processing Component Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.1 — Document Processing Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the component diagram showing structural interfaces for the Document Processing Foundation.

---

# Components

```mermaid
flowchart TD
    subgraph ServiceModule [Document Processing Subsystem]
        DPS[Document Processing Service]
        DPF[Document Parser Factory]
        DPR[Document Parser Registry]
        TN[Text Normalizer]
    end

    subgraph ParserImplementations [Extractors]
        PDF[PdfDocumentParser]
        DOCX[DocxDocumentParser]
    end

    subgraph ExternalLibraries [External Dependencies]
        fitz[PyMuPDF / fitz]
        docx[python-docx]
    end

    Client[Engine / Application Layer] -->|Call parse| DPS
    DPS --> DPF
    DPF --> DPR
    DPR -->|Resolves class| PDF
    DPR -->|Resolves class| DOCX
    DPS -->|Applies| TN
    
    PDF -->|Uses| fitz
    DOCX -->|Uses| docx
```
