# ATS Resume Intelligence Engine

# Book 06 — Evidence Intelligence

**Version:** 1.0

---

# Purpose

The Evidence Intelligence layer transforms Match Objects into structured, explainable evidence that is consumed by the ATS Scoring Engine.

Unlike the Hybrid Knowledge Layer, this module performs **no matching**. It simply explains and organizes the successful matches produced by Book 05.

Evidence becomes the foundation for

- ATS Score calculation
- Score explainability
- Requirement coverage
- Section analysis
- User recommendations
- API responses

This layer guarantees that every ATS score is backed by traceable evidence.

---

# Objectives

The Evidence Intelligence layer is responsible for

- Transforming Match Objects into Evidence Objects.
- Organizing evidence by Job Description requirements.
- Organizing evidence by Resume sections.
- Validating evidence.
- Measuring evidence confidence.
- Aggregating evidence.
- Producing explainable Evidence JSON.

---

# Scope

This book covers

- Evidence Generation
- Requirement Evidence
- Section Evidence
- Evidence Validation
- Evidence Confidence
- Evidence Aggregation
- Explainability Model
- Evidence JSON Specification

This book does not cover

- Resume Parsing
- Entity Extraction
- Feature Engineering
- Resume ↔ JD Matching
- ATS Scoring
- Resume Optimization

---

# Inputs

Consumes

- Match JSON

Produced by

Book 05 — Hybrid Knowledge Layer

---

# Outputs

Produces

- Evidence JSON

Consumed by

Book 07 — ATS Scoring Engine

---

# Evidence Philosophy

Evidence answers one question.

> **"Why did this Resume receive this ATS score?"**

Evidence never

- performs matching,
- modifies Match Objects,
- calculates ATS scores,
- applies penalties.

Its only responsibility is to organize and explain existing intelligence.

---

# Architecture

```
Match JSON

↓

Evidence Generation

↓

Requirement Evidence

↓

Section Evidence

↓

Evidence Validation

↓

Evidence Confidence

↓

Evidence Aggregation

↓

Explainability Model

↓

Evidence JSON
```

---

# Responsibilities

The Evidence Intelligence layer is responsible for

- Creating Evidence Objects.
- Recording supporting evidence.
- Organizing evidence by requirements.
- Organizing evidence by Resume sections.
- Measuring evidence confidence.
- Producing explainable evidence.
- Preserving traceability.

---

# Non-Responsibilities

The Evidence Intelligence layer never

- compares Resume and Job Description.
- executes Exact Matching.
- executes Alias Matching.
- executes Fuzzy Matching.
- executes Ontology Matching.
- executes Semantic Matching.
- calculates ATS scores.
- modifies Match JSON.

---

# Design Principles

## Explainable

Every Evidence Object must explain

- what matched,
- why it matched,
- where it matched.

---

## Deterministic

The same Match Objects must always produce the same Evidence Objects.

---

## Traceable

Every Evidence Object references the Match Object that created it.

No evidence may exist without a supporting Match Object.

---

## Immutable

Evidence Objects never modify

- Match Objects
- Feature JSON
- Entity JSON

---

## Single Source of Truth

Evidence is generated only once.

All downstream modules consume Evidence JSON.

No downstream module regenerates evidence.

---

# Evidence Categories

The Evidence Intelligence layer produces

## Requirement Evidence

Evidence grouped by Job Description requirements.

---

## Section Evidence

Evidence grouped by Resume sections.

---

## Aggregated Evidence

Combined evidence used for scoring.

---

## Explainability Evidence

Human-readable evidence for API responses.

---

# Processing Pipeline

```
Match JSON

↓

Evidence Object Creation

↓

Requirement Mapping

↓

Section Mapping

↓

Validation

↓

Confidence

↓

Aggregation

↓

Explainability

↓

Evidence JSON
```

---

# Evidence Lifecycle

```
Match Object

↓

Evidence Object

↓

Validated Evidence

↓

Confidence Added

↓

Aggregated Evidence

↓

Evidence JSON
```

---

# Evidence Object

Every Evidence Object contains

- Evidence ID
- Match Reference
- Requirement Reference
- Resume Section
- Evidence Type
- Evidence Description
- Evidence Confidence
- Metadata

---

# Evidence Rules

## Rule 1

Evidence must originate from a valid Match Object.

---

## Rule 2

Evidence must be deterministic.

---

## Rule 3

Evidence must never perform new matching.

---

## Rule 4

Evidence must preserve complete traceability.

---

## Rule 5

Evidence must never modify Match Objects.

---

## Rule 6

Each Match Object may produce multiple Evidence Objects.

Example

```
Python Match

↓

Requirement Evidence

↓

Skills Section Evidence

↓

Overall Evidence
```

---

## Rule 7

Every Evidence Object must have a unique identifier.

---

# Validation

Validate

- Missing Match References
- Duplicate Evidence IDs
- Invalid Requirement References
- Invalid Resume Sections
- Missing Confidence
- Broken Traceability

Return validation failures only.

---

# Confidence

Evidence Confidence is calculated after

- Matching Confidence
- Feature Confidence
- Entity Confidence

Evidence Confidence

- explains evidence reliability,
- never changes ATS Score.

---

# Explainability

Every Evidence Object must answer

- What matched?
- Why did it match?
- Which matching strategy was used?
- Which Resume section supports it?
- Which JD requirement supports it?
- How confident is the evidence?

---

# Dependencies

Consumes

- Match JSON

Produces

- Evidence JSON

Consumed by

- ATS Scoring Engine
- Output API
- Recommendation Engine
- Explainability Engine

---

# Related Files

- 01_Evidence_Generation.md
- 02_Requirement_Evidence.md
- 03_Section_Evidence.md
- 04_Evidence_Validation.md
- 05_Evidence_Confidence.md
- 06_Evidence_Aggregation.md
- 07_Explainability_Model.md
- 08_Evidence_JSON_Specification.md

---

# End of Book 06