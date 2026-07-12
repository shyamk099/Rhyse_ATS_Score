# ATS Resume Intelligence Engine

# Evidence Aggregation

**Version:** 1.0

---

# Purpose

The Evidence Aggregation Engine consolidates all validated Evidence Objects into a unified Evidence Model for ATS scoring.

Unlike previous modules, which organize evidence by requirement or Resume section, this module creates a complete evidence view of the Resume ↔ Job Description comparison.

Evidence Aggregation performs no matching and no ATS scoring.

---

# Objectives

The Evidence Aggregation Engine must

- Aggregate all validated evidence.
- Remove duplicate evidence.
- Preserve traceability.
- Organize evidence for ATS Scoring.
- Produce deterministic Aggregated Evidence.

---

# Scope

This module covers

- Requirement Aggregation
- Section Aggregation
- Global Aggregation
- Evidence Deduplication
- Evidence Prioritization
- Aggregated Evidence Generation

This module does not cover

- Resume Matching
- ATS Scoring
- Resume Optimization

---

# Inputs

Consumes

- Requirement Evidence
- Section Evidence
- Validated Evidence
- Evidence Confidence

Produced by

- Requirement Evidence
- Section Evidence
- Evidence Validation
- Evidence Confidence

---

# Outputs

Produces

- Aggregated Evidence

Consumed by

- ATS Scoring Engine
- Explainability Engine
- Output API

---

# Processing Pipeline

```
Requirement Evidence

+

Section Evidence

+

Validated Evidence

↓

Evidence Merge

↓

Duplicate Detection

↓

Evidence Prioritization

↓

Aggregation

↓

Aggregated Evidence
```

---

# Aggregation Philosophy

Aggregation answers one question.

> "What is the complete evidence supporting this Resume?"

The objective is to provide one unified evidence model for downstream scoring.

Aggregation never performs matching.

Aggregation never creates new evidence.

Aggregation never modifies Evidence Objects.

---

# Aggregation Levels

## Level 1

Requirement Aggregation

Groups evidence by Job Description requirement.

---

## Level 2

Section Aggregation

Groups evidence by Resume section.

---

## Level 3

Global Aggregation

Combines all evidence into a unified evidence collection.

---

# Evidence Prioritization

When duplicate evidence exists, the highest quality evidence is retained.

Priority order

```
Exact Match

↓

Alias Match

↓

Ontology Match

↓

Fuzzy Match

↓

Semantic Match
```

If multiple Evidence Objects represent the same business fact, only the highest-priority evidence is retained in the aggregated view.

Original Evidence Objects remain unchanged.

---

# Duplicate Detection

Duplicate evidence is identified using

- Match ID
- Requirement ID
- Resume Feature ID
- JD Feature ID
- Evidence Type

Duplicates are grouped before prioritization.

---

# Aggregated Evidence

The Aggregated Evidence contains

- Requirement Summary
- Resume Section Summary
- Overall Evidence Summary
- Coverage Metrics
- Evidence Confidence Summary

---

# Coverage Metrics

Aggregation calculates

- Requirement Coverage
- Section Coverage
- Skill Coverage
- Experience Coverage
- Certification Coverage
- Project Coverage

Coverage metrics are descriptive only.

They never calculate ATS Score.

---

# Summary Metrics

The aggregated model records

- Total Evidence
- Total Matches
- Total Requirements Covered
- Total Resume Sections Contributing
- Overall Evidence Confidence

---

# Aggregation Rules

## Rule 1

Aggregation never modifies original Evidence Objects.

---

## Rule 2

Aggregation never performs matching.

---

## Rule 3

Aggregation never calculates ATS scores.

---

## Rule 4

Aggregation preserves complete traceability.

---

## Rule 5

Every Aggregated Evidence object references its source Evidence Objects.

---

## Rule 6

Duplicate Evidence is consolidated only in the aggregated view.

---

## Rule 7

Aggregation must be deterministic.

---

# Validation

Validate

- Missing Evidence Objects
- Missing Requirement Groups
- Missing Section Groups
- Duplicate References
- Invalid Aggregation Results

Return validation failures only.

---

# Aggregated Evidence Structure

Each Aggregated Evidence object contains

- Aggregation ID
- Evidence IDs
- Requirement Summary
- Section Summary
- Coverage Metrics
- Confidence Summary
- Metadata

---

# Example

```
Requirement Evidence

↓

Python

↓

AWS

↓

Docker

+

Section Evidence

↓

Experience

↓

Projects

↓

Skills

↓

Aggregated Evidence

↓

Coverage Summary
```

---

# Non-Functional Requirements

The Aggregation Engine must be

- Deterministic
- Stateless
- Explainable
- Auditable
- Repeatable

---

# Dependencies

Consumes

- Requirement Evidence
- Section Evidence
- Validated Evidence
- Evidence Confidence

Produces

- Aggregated Evidence

Consumed by

- ATS Scoring Engine
- Explainability Engine
- Output API

---

# Related Files

- Book_06_Evidence_Intelligence.md
- Evidence_Generation.md
- Requirement_Evidence.md
- Section_Evidence.md
- Evidence_Validation.md
- Evidence_Confidence.md
- Explainability_Model.md
- Evidence_JSON_Specification.md

---

# End of Evidence Aggregation