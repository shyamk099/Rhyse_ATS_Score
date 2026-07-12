# ATS Resume Intelligence Engine

# Resume Parser

**Version:** 1.0

---

# Purpose

The Resume Parser converts an uploaded resume into a standardized JSON representation.

It is responsible only for parsing the document structure.

It does not perform

- ATS Scoring
- Entity Extraction
- Semantic Matching
- Resume Quality Analysis

---

# Objectives

The parser must

- Parse supported resume formats.
- Detect resume sections.
- Preserve document structure.
- Normalize extracted text.
- Produce deterministic JSON.
- Report parser confidence.

---

# Supported Formats

## Supported

- PDF
- DOCX

---

## Future

- HTML
- TXT
- LinkedIn Export

---

# Processing Pipeline

```
Resume

↓

File Validation

↓

File Type Detection

↓

OCR Detection

↓

Text Extraction

↓

Resume Parser

↓

Section Detection

↓

JSON Builder

↓

Resume JSON
```

---

# Parser Responsibilities

The parser identifies the following sections.

## Personal Information

- Full Name
- Email
- Phone
- Location
- LinkedIn
- GitHub
- Portfolio

---

## Professional Summary

Candidate summary.

---

## Skills

Technical

Soft Skills

Tools

Frameworks

Platforms

Languages

---

## Experience

Each experience contains

- Company
- Job Title
- Employment Type
- Location
- Start Date
- End Date
- Current Position
- Responsibilities

---

## Projects

Each project contains

- Project Name
- Description
- Technologies
- Responsibilities

---

## Education

Each education entry contains

- Degree
- Institution
- Location
- Graduation Date

---

## Certifications

Each certification contains

- Certification Name
- Organization
- Issue Date
- Expiration Date

---

## Awards

Optional

---

## Publications

Optional

---

## Languages

Optional

---

# Parsing Rules

## Rule 1

Never infer information.

Only parse what exists.

---

## Rule 2

Preserve original wording.

Do not rewrite.

---

## Rule 3

Do not classify skills.

Classification belongs to Entity Extraction.

---

## Rule 4

Do not calculate years of experience.

Feature Engineering performs calculations.

---

## Rule 5

Do not merge duplicated sections.

Preserve source data.

---

# Output JSON

```
Resume

↓

Metadata

↓

Sections

↓

Raw Text

↓

Structured Fields
```

---

# Validation Rules

Validate

- Empty resume
- Missing contact section
- Invalid email
- Invalid dates
- Corrupted structure

Produce warnings instead of modifying content.

---

# Parser Confidence

Parser Confidence measures how successfully the document was parsed.

Example

```
98%

↓

All sections identified.

------------------------

62%

↓

Experience section partially parsed.
```

Parser Confidence never affects ATS Score.

---

# Error Handling

Possible errors

- Unsupported format
- OCR failure
- Corrupted PDF
- Empty document
- Parsing failure

Each error should return

- Error Code
- Error Message
- Suggested Action

---

# Inputs

Resume Document

---

# Outputs

Resume JSON

Parser Confidence

Validation Report

---

# Dependencies

Depends on

- Book 01

Provides input to

- Entity Extraction

---

# Related Files

- Book_02_Document_Processing.md
- OCR_Processing.md
- Text_Extraction.md
- JSON_Schemas.md

---

# End of Resume Parser