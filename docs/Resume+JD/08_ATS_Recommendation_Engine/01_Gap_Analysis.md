# ATS Resume Intelligence Engine

# Gap Analysis

**Version:** 1.0

---

# Purpose

The Gap Analysis Engine identifies all deficiencies between the Resume and the Job Description using the intelligence produced by previous books.

Its responsibility is to detect missing, weak, incomplete, or unsupported areas that prevent the Resume from achieving a higher ATS Score.

Gap Analysis never performs Resume rewriting.

Gap Analysis never recalculates ATS scores.

---

# Objectives

The Gap Analysis Engine must

- Detect Requirement Gaps.
- Detect Evidence Gaps.
- Detect Coverage Gaps.
- Detect Quality Gaps.
- Produce deterministic Gap Objects.

---

# Scope

This module covers

- Requirement Gap Analysis
- Evidence Gap Analysis
- Coverage Gap Analysis
- Quality Gap Analysis
- Gap Classification

This module does not cover

- Resume Rewriting
- Resume Optimization
- ATS Scoring
- Resume Matching

---

# Inputs

Consumes

- Evidence JSON
- Score JSON

Produced by

Book 06

Book 07

---

# Outputs

Produces

- Gap Objects

Consumed by

- Recommendation Generation
- Recommendation Prioritization

---

# Processing Pipeline

```
Evidence JSON

+

Score JSON

↓

Requirement Analysis

↓

Evidence Analysis

↓

Coverage Analysis

↓

Quality Analysis

↓

Gap Classification

↓

Gap Objects
```

---

# Gap Philosophy

Gap Analysis answers one question.

> "What is preventing this Resume from receiving a higher ATS Score?"

Every identified gap must be supported by evidence.

No assumptions are permitted.

---

# Gap Categories

## Requirement Gap

A Job Description requirement is not satisfied.

Examples

- Missing Skill
- Missing Certification
- Missing Experience
- Missing Responsibility

---

## Evidence Gap

The Resume claims a skill but provides insufficient supporting evidence.

Examples

```
Python listed

↓

No Experience

↓

No Projects
```

---

## Coverage Gap

The Resume satisfies the requirement only partially.

Examples

```
JD

Python

Docker

Spark

AWS

↓

Resume

Python

Spark

↓

Coverage

50%
```

---

## Quality Gap

The Resume contains evidence, but the evidence is weak.

Examples

- Weak project descriptions
- Generic experience bullets
- Missing measurable achievements
- Low-quality professional summary

---

## ATS Compatibility Gap

The Resume contains ATS-unfriendly formatting.

Examples

- Tables
- Images
- Text Boxes
- Missing Section Headers

---

# Gap Severity

Every Gap receives one severity.

- Critical
- High
- Medium
- Low

Severity depends on

- Requirement importance
- Score impact
- Coverage loss

---

# Gap Object

Every Gap contains

- Gap ID
- Gap Type
- Severity
- Related Requirement
- Related Resume Section
- Supporting Evidence
- Missing Evidence
- Description

---

# Example

```
Requirement

Apache Spark

↓

Evidence

None

↓

Gap

Requirement Gap

↓

Severity

Critical
```

---

Another Example

```
Requirement

Python

↓

Evidence

Skills Only

↓

Projects

Missing

↓

Experience

Missing

↓

Gap

Evidence Gap
```

---

# Gap Rules

## Rule 1

Every Gap must reference at least one Requirement.

---

## Rule 2

Every Gap must reference supporting Evidence.

---

## Rule 3

Gap Analysis never invents missing skills.

---

## Rule 4

Gap Analysis never performs Resume Matching.

---

## Rule 5

Gap Analysis never modifies Evidence JSON.

---

## Rule 6

Gap Analysis must always be deterministic.

---

## Rule 7

Every Gap receives exactly one severity.

---

# Validation

Validate

- Duplicate Gaps
- Missing Requirement References
- Missing Evidence References
- Invalid Severity
- Invalid Gap Type

Return validation failures only.

---

# Gap Output

Produces

- Gap Objects
- Gap Summary
- Severity Summary
- Coverage Summary

---

# Dependencies

Consumes

- Evidence JSON
- Score JSON

Produces

- Gap Objects

Consumed by

- Recommendation Generation
- Recommendation Prioritization

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- Recommendation_Generation.md
- Recommendation_Prioritization.md
- Score_Impact_Estimation.md
- Recommendation_Validation.md
- Recommendation_JSON_Specification.md
- Recommendation_API_Contract.md

---

# End of Gap Analysis