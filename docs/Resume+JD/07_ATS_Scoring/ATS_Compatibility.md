# ATS Resume Intelligence Engine

# ATS Compatibility Score

**Version:** 1.0

---

# Purpose

The ATS Compatibility Score measures how well a Resume can be parsed and processed by modern Applicant Tracking Systems (ATS).

This score evaluates the Resume's technical compatibility with ATS software.

It does not evaluate Resume quality or Job Description matching.

---

# Objectives

The ATS Compatibility Score must

- Measure ATS readability.
- Measure parsing compatibility.
- Measure Resume structure.
- Detect ATS-unfriendly formatting.
- Produce a deterministic score.

---

# Scope

This module covers

- Resume Structure
- Resume Formatting
- ATS Parsing Compatibility
- Section Recognition
- File Compatibility
- Text Accessibility

This module does not cover

- Resume Quality
- Resume–JD Matching
- Semantic Matching
- Resume Optimization

---

# Inputs

Consumes

- Resume Feature JSON
- Evidence JSON

Produced by

- Feature Engineering
- Evidence Intelligence

---

# Outputs

Produces

- ATS Compatibility Score

Consumed by

- Weighted Scoring Engine

---

# Scoring Philosophy

The ATS Compatibility Score answers one question.

> "Can an ATS successfully parse and understand this Resume?"

This score measures technical compatibility only.

It does not measure candidate quality.

---

# Evaluation Categories

## Resume Structure

Checks

- Standard Resume Layout
- Logical Section Order
- Section Consistency

---

## Section Recognition

Checks

- Summary
- Skills
- Experience
- Projects
- Education
- Certifications

Sections must be clearly identifiable.

---

## Formatting Compatibility

Checks

- Tables
- Columns
- Images
- Icons
- Text Boxes
- Headers
- Footers

Formatting should remain ATS-friendly.

---

## File Compatibility

Checks

- Supported File Format
- Readable Text
- Character Encoding

---

## Text Accessibility

Checks

- Selectable Text
- Hidden Text
- White Text
- Embedded Images
- OCR Dependency

---

# ATS Compatibility Components

The ATS Compatibility Score consists of

- Structure Score
- Section Score
- Formatting Score
- File Compatibility Score
- Text Accessibility Score

---

# Scoring Rules

## Rule 1

Only Resume characteristics are evaluated.

---

## Rule 2

Job Description is never considered.

---

## Rule 3

ATS Compatibility never evaluates candidate skills.

---

## Rule 4

ATS Compatibility never evaluates experience relevance.

---

## Rule 5

The score must be deterministic.

---

# Example

```
Resume

↓

Well Structured

↓

Recognizable Sections

↓

ATS-Friendly Formatting

↓

No Hidden Text

↓

ATS Compatibility

96%
```

---

Another Example

```
Resume

↓

Multiple Tables

↓

Image-Based Text

↓

Unrecognized Sections

↓

ATS Compatibility

58%
```

---

# Validation

Validate

- Missing Resume Sections
- Unsupported File Types
- Parsing Errors
- Hidden Text
- Invalid Formatting

Return validation failures only.

---

# Score Output

Produces

- ATS Compatibility Score
- Compatibility Level
- Detected Issues
- Improvement Areas

---

# Dependencies

Consumes

- Resume Feature JSON
- Evidence JSON

Produces

- ATS Compatibility Score

Consumed by

- Weighted Scoring Engine

---

# Related Files

- Book_07_ATS_Scoring.md
- Resume_Quality_Score.md
- Resume_JD_Match_Score.md
- Weighted_Scoring_Engine.md
- Score_JSON_Specification.md

---

# End of ATS Compatibility Score