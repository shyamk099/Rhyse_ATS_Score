# ATS Resume Intelligence Engine

# Job Description Parser

**Version:** 1.0

---

# Purpose

The Job Description Parser converts a Job Description into a standardized JSON representation.

Its responsibility is to extract and preserve the hiring requirements exactly as they appear in the source document.

The parser does not perform

- Resume Matching
- Skill Classification
- ATS Scoring
- Semantic Matching
- Requirement Prioritization

---

# Objectives

The parser must

- Parse supported JD formats.
- Detect logical sections.
- Preserve original wording.
- Produce deterministic JSON.
- Report parser confidence.
- Validate extracted content.

---

# Supported Formats

## Supported

- PDF
- DOCX
- Plain Text

---

## Future

- HTML
- Company Career Pages
- LinkedIn Jobs
- Indeed Jobs
- Greenhouse
- Lever
- Workday

---

# Processing Pipeline

```
Job Description

↓

File Validation

↓

File Type Detection

↓

OCR Detection

↓

Text Extraction

↓

JD Parser

↓

Section Detection

↓

JSON Builder

↓

Structured JD JSON
```

---

# Parser Responsibilities

The parser extracts the following sections.

## Job Information

- Job Title
- Department
- Employment Type
- Work Mode
- Location

---

## Job Summary

Overall description of the role.

---

## Responsibilities

List of responsibilities exactly as written.

---

## Required Skills

Skills explicitly marked as required.

---

## Preferred Skills

Skills marked as preferred or nice to have.

---

## Experience Requirements

Examples

- Years of Experience
- Industry Experience
- Domain Experience

---

## Education Requirements

Examples

- Degree
- Field of Study

---

## Certifications

Required or preferred certifications.

---

## Technical Stack

Examples

- Programming Languages
- Frameworks
- Databases
- Cloud Platforms
- Tools

---

## Soft Skills

Examples

- Communication
- Leadership
- Collaboration

---

## Benefits

Optional

---

## Additional Information

Optional

---

# Parsing Rules

## Rule 1

Never infer missing requirements.

Only parse explicitly stated information.

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

Do not determine mandatory vs optional unless explicitly stated.

---

## Rule 5

Do not merge duplicated requirements.

Preserve source data.

---

# Output JSON

```
Job Description

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

- Empty document
- Missing title
- Missing responsibilities
- Corrupted structure
- Invalid formatting

Validation generates warnings only.

---

# Parser Confidence

Parser Confidence measures how successfully the document was parsed.

Example

```
97%

↓

All sections successfully parsed.

------------------------

61%

↓

Responsibilities partially extracted.
```

Parser Confidence never affects ATS Score.

---

# Error Handling

Possible errors

- Unsupported format
- OCR failure
- Corrupted document
- Empty document
- Parsing failure

Each error should return

- Error Code
- Error Message
- Suggested Action

---

# Inputs

Job Description Document

---

# Outputs

Structured JD JSON

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
- Resume_Parser.md
- OCR_Processing.md
- Text_Extraction.md
- JSON_Schemas.md

---

# End of Job Description Parser