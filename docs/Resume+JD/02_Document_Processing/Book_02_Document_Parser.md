# ATS Resume Intelligence Engine

# Book 02 — Document Processing

**Version:** 1.0

---

# Purpose

The Document Processing layer is responsible for converting uploaded Resume and Job Description documents into standardized, machine-readable JSON objects.

This layer ensures that every downstream component receives consistent and validated input regardless of document format.

This layer performs no scoring, matching, or semantic analysis.

---

# Objectives

The Document Processing layer is responsible for:

- Accepting supported document formats.
- Extracting readable text.
- Handling scanned documents.
- Parsing document structure.
- Producing normalized JSON.
- Validating document integrity.
- Reporting parsing confidence.

---

# Scope

This book covers

- Document Ingestion
- Resume Parsing
- Job Description Parsing
- OCR Processing
- Text Extraction
- JSON Generation

This book does **not** cover

- Entity Extraction
- Feature Engineering
- ATS Scoring
- Semantic Matching
- Resume Optimization

---

# Supported Document Types

## Resume

- PDF
- DOCX

Future

- TXT
- HTML
- LinkedIn Export

---

## Job Description

- PDF
- DOCX
- Plain Text

Future

- Company Career Page
- LinkedIn Job
- Indeed Job
- API Sources

---

# Processing Pipeline

```
Document Upload

↓

File Validation

↓

File Type Detection

↓

OCR Detection

↓

Text Extraction

↓

Parser

↓

Document Validation

↓

Structured JSON
```

---

# Layer Responsibilities

## 1. Document Upload

Receives documents from

- REST API
- Web UI
- Batch Processing

Output

Binary Document

---

## 2. File Validation

Validates

- File Extension
- File Size
- Corrupted Files
- Password Protection

Output

Validated Document

---

## 3. File Type Detection

Identifies

- PDF
- DOCX
- Image-based PDF
- Text-based PDF

Output

Document Type

---

## 4. OCR Detection

Determines whether OCR is required.

Decision

```
Image PDF

↓

OCR Required

-------------------

Text PDF

↓

OCR Not Required
```

---

## 5. Text Extraction

Extracts

- Paragraphs
- Lists
- Tables (if supported)
- Headers

Output

Raw Text

---

## 6. Parser

Converts raw text into structured sections.

Resume

- Contact
- Summary
- Skills
- Experience
- Projects
- Education
- Certifications

Job Description

- Title
- Skills
- Responsibilities
- Requirements
- Qualifications

Output

Structured JSON

---

## 7. Validation

Checks

- Missing Sections
- Invalid Dates
- Empty Documents
- Parsing Errors

Produces

Validation Report

---

# Inputs

Resume

Job Description

---

# Outputs

Structured Resume JSON

Structured JD JSON

Validation Report

Parser Confidence

---

# Non-Functional Requirements

The processing layer must be

- Deterministic
- Repeatable
- Fast
- Stateless
- Explainable
- Extensible

---

# Error Handling

Examples

- Unsupported File Type
- Corrupted Document
- Empty Document
- OCR Failure
- Parsing Failure

Errors should be descriptive and recoverable whenever possible.

---

# Dependencies

Depends on

- Book 00
- Book 01

Provides input for

- Book 03 — Entity Extraction

---

# Related Files

- Resume_Parser.md
- JD_Parser.md
- OCR_Processing.md
- Text_Extraction.md
- JSON_Schemas.md

---

# End of Book 02