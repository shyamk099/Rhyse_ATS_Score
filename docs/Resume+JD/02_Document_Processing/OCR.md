# ATS Resume Intelligence Engine

# OCR Processing

**Version:** 1.0

---

# Purpose

The OCR Processing module converts image-based documents into machine-readable text.

Its responsibility is limited to text recognition.

It does not

- Parse sections
- Extract entities
- Normalize data
- Perform ATS scoring

---

# Objectives

The OCR engine must

- Detect scanned documents.
- Convert images into text.
- Preserve document reading order.
- Preserve line structure.
- Preserve page order.
- Produce deterministic output.
- Report OCR confidence.

---

# Scope

This module handles

- Image-based PDFs
- Scanned resumes
- Scanned Job Descriptions

This module does not handle

- Text parsing
- Section detection
- Entity extraction
- Feature engineering

---

# Supported Inputs

Supported

- Image PDF
- JPEG
- PNG
- TIFF

Future

- HEIC
- BMP

---

# Processing Pipeline

```
Document

↓

Document Type Detection

↓

Image Detection

↓

OCR Required?

↓

Yes

↓

OCR Engine

↓

Extracted Text

↓

OCR Validation

↓

Raw Text
```

---

# OCR Detection

The system determines whether OCR is required.

Decision

```
Text PDF

↓

OCR = No

-----------------------

Image PDF

↓

OCR = Yes
```

---

# OCR Responsibilities

The OCR engine must

- Read visible text.
- Preserve paragraph boundaries.
- Preserve bullet lists.
- Preserve line breaks.
- Preserve page sequence.

---

# OCR Rules

## Rule 1

Never modify recognized text.

---

## Rule 2

Never infer missing words.

---

## Rule 3

Never correct grammar.

---

## Rule 4

Never classify content.

---

## Rule 5

Preserve extraction order.

---

# OCR Confidence

OCR produces a confidence score.

Example

```
99%

↓

Clean scan

----------------------

63%

↓

Blurred scan

----------------------

28%

↓

Unreadable scan
```

OCR confidence never changes ATS score.

---

# Validation

Validate

- Blank pages
- Corrupted scans
- Low-quality images
- Unsupported formats
- OCR failures

Generate warnings only.

---

# Error Handling

Possible errors

- OCR Timeout
- OCR Failure
- Unsupported Image
- Corrupted Scan
- Empty Image

Return

- Error Code
- Error Message
- Suggested Resolution

---

# Inputs

Image Document

---

# Outputs

Extracted Text

OCR Confidence

Validation Report

---

# Dependencies

Provides input to

- Text Extraction
- Resume Parser
- JD Parser

Depends on

- Document Processing

---

# Non-Functional Requirements

The OCR module must be

- Deterministic
- Stateless
- Scalable
- Language-independent
- Recoverable

---

# Related Files

- Book_02_Document_Processing.md
- Resume_Parser.md
- JD_Parser.md
- Text_Extraction.md
- JSON_Schemas.md

---

# End of OCR Processing