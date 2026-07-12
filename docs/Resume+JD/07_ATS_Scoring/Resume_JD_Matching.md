# ATS Resume Intelligence Engine

# Resume–JD Match Score

**Version:** 1.0

---

# Purpose

The Resume–JD Match Score measures how well the Resume satisfies the requirements defined in the Job Description.

Unlike the ATS Compatibility Score and Resume Quality Score, this component evaluates Resume relevance against a specific Job Description.

The Resume–JD Match Score is calculated entirely from validated Evidence JSON.

No Resume ↔ JD matching is performed inside this module.

---

# Objectives

The Resume–JD Match Score must

- Measure Resume relevance.
- Measure Job Requirement Coverage.
- Measure Skill Alignment.
- Measure Experience Alignment.
- Measure Qualification Alignment.
- Produce a deterministic score.

---

# Scope

This module covers

- Requirement Coverage
- Skill Matching
- Experience Matching
- Education Matching
- Certification Matching
- Responsibility Matching

This module does not cover

- Resume Parsing
- Resume Quality
- ATS Compatibility
- Semantic Matching
- Resume Optimization

---

# Inputs

Consumes

- Evidence JSON

Produced by

Book 06 — Evidence Intelligence

---

# Outputs

Produces

- Resume–JD Match Score

Consumed by

- Weighted Scoring Engine

---

# Design Philosophy

The Resume–JD Match Score answers one question.

> "How well does this Resume satisfy this specific Job Description?"

This score is based entirely on validated evidence.

No matching engine is executed here.

---

# Processing Pipeline

```
Evidence JSON

↓

Requirement Analysis

↓

Coverage Analysis

↓

Component Scores

↓

Resume–JD Match Score
```

---

# Match Components

The Resume–JD Match Score consists of

- Requirement Coverage
- Skill Alignment
- Experience Alignment
- Education Alignment
- Certification Alignment
- Responsibility Alignment

---

# Requirement Coverage

Measures

- Mandatory Requirements Matched
- Preferred Requirements Matched
- Optional Requirements Matched

Coverage is calculated from

Requirement Evidence.

---

# Skill Alignment

Measures

- Required Skills Found
- Preferred Skills Found
- Missing Skills

Evidence Source

Requirement Evidence

---

# Experience Alignment

Measures

- Years of Experience
- Relevant Experience
- Domain Experience
- Leadership Experience

Evidence Source

Section Evidence

---

# Education Alignment

Measures

- Required Degrees
- Preferred Degrees
- Academic Qualifications

Evidence Source

Requirement Evidence

---

# Certification Alignment

Measures

- Required Certifications
- Preferred Certifications

Evidence Source

Requirement Evidence

---

# Responsibility Alignment

Measures

- Responsibilities matched.
- Business functions covered.
- Technical responsibilities covered.

Evidence Source

Requirement Evidence

---

# Match Levels

Each requirement receives one status.

- Fully Matched
- Partially Matched
- Not Matched
- Not Applicable

---

# Scoring Rules

## Rule 1

Only validated Evidence JSON may be consumed.

---

## Rule 2

Resume–JD Matching is never executed.

---

## Rule 3

Only Requirement Evidence may determine requirement coverage.

---

## Rule 4

Missing evidence never creates assumptions.

---

## Rule 5

Resume–JD Match Score must always be deterministic.

---

# Example

```
Job Description

↓

24 Requirements

↓

22 Requirements Supported

↓

Requirement Coverage

91.7%

↓

Resume–JD Match Score
```

---

Another Example

```
Required Skills

10

↓

Matched

7

↓

Missing

3

↓

Skill Alignment

70%
```

---

# Validation

Validate

- Missing Requirement Evidence
- Missing Section Evidence
- Invalid Coverage Values
- Duplicate Requirements
- Missing Evidence References

Return validation failures only.

---

# Score Output

Produces

- Resume–JD Match Score
- Requirement Coverage
- Skill Alignment
- Experience Alignment
- Education Alignment
- Certification Alignment
- Responsibility Alignment

---

# Design Decisions

The Resume–JD Match Score

- consumes Evidence JSON,
- never consumes Match JSON,
- never consumes Feature JSON,
- never performs semantic matching,
- never performs ontology traversal.

All intelligence has already been completed in previous books.

---

# Dependencies

Consumes

- Evidence JSON

Produces

- Resume–JD Match Score

Consumed by

- Weighted Scoring Engine

---

# Related Files

- Book_07_ATS_Scoring.md
- ATS_Compatibility_Score.md
- Resume_Quality_Score.md
- Semantic_Validation_Score.md
- Weighted_Scoring_Engine.md
- Score_JSON_Specification.md

---

# End of Resume–JD Match Score