# ATS Resume Intelligence Engine

# Text Extraction

**Version:** 1.0

---

# Purpose

The Text Extraction module converts supported documents into a deterministic text representation while preserving the logical reading order.

Its responsibility ends with producing clean, structured text.

It does not

- Detect sections
- Classify content
- Extract entities
- Normalize values
- Perform semantic analysis
- Calculate ATS scores

---

# Objectives

The Text Extraction module must

- Extract readable text.
- Preserve logical reading order.
- Preserve paragraph boundaries.
- Preserve bullet lists.
- Preserve page order.
- Preserve document structure.
- Produce deterministic output.

---

# Scope

This module processes

- Text-based PDF
- DOCX
- OCR Output

This module does not process

- Images directly
- Section Detection
- Entity Extraction
- Feature Engineering

---

# Processing Pipeline

```
Document

↓

Text Detection

↓

Text Extraction

↓

Cleaning

↓

Structure Preservation

↓

Validation

↓

Raw Text Object
```

---

# Responsibilities

The module is responsible for

- Reading document text
- Preserving reading order
- Preserving paragraphs
- Preserving bullet points
- Preserving line breaks
- Preserving page sequence

---

# Text Cleaning Rules

The extraction module performs only safe normalization.

Allowed

- Remove duplicated whitespace
- Normalize line endings
- Normalize Unicode encoding
- Remove non-printable control characters

Not Allowed

- Grammar correction
- Spell correction
- Sentence rewriting
- Skill normalization
- Section detection
- Date normalization
- Phone normalization
- URL normalization

Those belong to later processing stages.

---

# Reading Order

The extracted text must preserve the logical reading order.

Example

```
Name

↓

Summary

↓

Skills

↓

Experience

↓

Education
```

The extraction module must not reorder content.

---

# Tables

If tables exist

Extract

- Row order
- Cell text

Do not infer relationships.

---

# Hyperlinks

Extract

Visible Text

URL

Example

```
LinkedIn

↓

https://linkedin.com/in/example
```

---

# Lists

Preserve

- Bullet lists
- Numbered lists
- Nested lists

Do not flatten them.

---

# Metadata

The module may preserve metadata for future use.

Optional Metadata

- Page Number
- Paragraph Index
- Line Number
- Bounding Box (if available)

Metadata is not consumed by ATS scoring in Version 1.

---

# Validation

Validate

- Empty text
- Corrupted characters
- Encoding issues
- Missing pages
- Extraction failures

Return warnings only.

---

# Output

The module produces a Raw Text Object.

```
Raw Text Object

↓

Text

↓

Metadata

↓

Validation Report
```

---

# Text Object

Contains

- Raw Text
- Source Type
- Page Count
- Metadata
- Validation Report

---

# Error Handling

Possible Errors

- Unsupported Encoding
- Corrupted PDF
- Empty Document
- Extraction Failure

Each error returns

- Error Code
- Error Message
- Suggested Resolution

---

# Non-Functional Requirements

The Text Extraction module must be

- Deterministic
- Stateless
- Repeatable
- Scalable
- Language Independent

---

# Dependencies

Consumes

- OCR Output
- PDF
- DOCX

Provides

- Resume Parser
- JD Parser

---

# Related Files

- Book_02_Document_Processing.md
- Resume_Parser.md
- JD_Parser.md
- OCR_Processing.md
- JSON_Schemas.md

---

# End of Text Extraction