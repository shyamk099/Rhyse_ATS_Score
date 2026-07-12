# ATS Resume Intelligence Engine

# Book 05 — Hybrid Knowledge Layer

**Version:** 1.0

---

# Purpose

The Hybrid Knowledge Layer is the intelligence core of the ATS Resume Intelligence Engine.

Its responsibility is to determine whether entities and features extracted from the Resume and Job Description represent the same business concept.

Unlike previous layers, this layer performs intelligent matching using multiple matching strategies while maintaining deterministic and explainable behavior.

This layer does not calculate ATS scores.

---

# Objectives

The Hybrid Knowledge Layer is responsible for

- Comparing Resume Features with Job Description Features.
- Applying deterministic matching strategies.
- Producing explainable match results.
- Recording match confidence.
- Producing reusable Match Objects.

---

# Scope

This book covers

- Exact Matching
- Alias Matching
- Fuzzy Matching
- Ontology Matching
- Semantic Matching
- Matching Pipeline
- Matching Confidence
- Match JSON Specification

This book does not cover

- ATS Scoring
- Evidence Generation
- Resume Optimization

---

# Inputs

Consumes

- Resume Feature JSON
- JD Feature JSON

Produced by

- Book 04 — Feature Engineering

---

# Outputs

Produces

- Match JSON

Consumed by

- Book 06 — Evidence Intelligence

---

# Matching Philosophy

Matching follows a deterministic hierarchy.

Higher-confidence methods always execute before lower-confidence methods.

The first successful match is accepted according to business rules.

---

# Matching Hierarchy

```
Resume Feature

↓

Exact Match

↓

Alias Match

↓

Fuzzy Match

↓

Ontology Match

↓

Semantic Match

↓

Match Object
```

---

# Matching Strategies

## Exact Matching

Determines whether two normalized values are identical.

Example

```
Python

↓

Python
```

---

## Alias Matching

Determines whether two values are officially recognized aliases.

Example

```
JS

↓

JavaScript
```

---

## Fuzzy Matching

Determines whether two values are typographical variations.

Example

```
Postgre SQL

↓

PostgreSQL
```

---

## Ontology Matching

Determines whether two entities are related within the Technology Ontology.

Example

```
Amazon EMR

↓

AWS
```

---

## Semantic Matching

Determines contextual similarity using embeddings.

Semantic Matching executes only if all previous strategies fail.

Semantic Matching never replaces Exact, Alias, Fuzzy, or Ontology Matching.

---

# Matching Order

The execution order is fixed.

```
Exact

↓

Alias

↓

Fuzzy

↓

Ontology

↓

Semantic
```

The order must never change unless the Algorithm Version changes.

---

# Design Principles

## Deterministic

Matching must always produce identical results for identical inputs.

---

## Explainable

Every successful match must record

- Matching Strategy
- Match Reason
- Confidence

---

## Single Match Engine

Every comparison passes through the same matching pipeline.

No engine performs independent matching.

---

## Single Source of Truth

Every successful match produces a Match Object.

Downstream engines consume Match Objects rather than recalculating matches.

---

# Responsibilities

The Hybrid Knowledge Layer is responsible for

- Feature Comparison
- Strategy Selection
- Match Validation
- Match Confidence
- Match Generation

---

# Non-Responsibilities

The Hybrid Knowledge Layer does not

- Calculate ATS Scores
- Generate Evidence
- Apply Integrity Penalties
- Modify Feature JSON

---

# Processing Pipeline

```
Resume Feature JSON

+

JD Feature JSON

↓

Matching Pipeline

↓

Matching Strategy

↓

Match Validation

↓

Match Confidence

↓

Match JSON
```

---

# Matching Rules

Rule 1

Higher-confidence strategies execute before lower-confidence strategies.

---

Rule 2

Matching must be deterministic.

---

Rule 3

Every successful match records its strategy.

---

Rule 4

Every unsuccessful comparison is recorded.

---

Rule 5

Matching never modifies Feature JSON.

---

# Dependencies

Consumes

- Feature JSON

Produces

- Match JSON

Consumed by

- Book 06 — Evidence Intelligence

---

# Related Files

- Exact_Matching.md
- Alias_Matching.md
- Fuzzy_Matching.md
- Ontology_Matching.md
- Semantic_Matching.md
- Technology_Ontology.md
- Alias_Dictionary.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Match_JSON_Specification.md

---

# End of Book 05