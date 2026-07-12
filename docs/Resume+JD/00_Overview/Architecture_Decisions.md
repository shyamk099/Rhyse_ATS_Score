# ATS Resume Intelligence Engine

# Architecture Decision Records (ADR)

**Version:** 1.0

---

# Purpose

This document records the major architectural decisions made during the design of the ATS Resume Intelligence Engine.

The objective is to explain **why** each decision was made, what alternatives were considered, and the expected impact on the overall system.

These decisions should remain stable unless there is strong technical justification to change them.

---

# ADR-001

## Deterministic Scoring

### Decision

The ATS scoring engine shall be deterministic.

Given the same Resume, Job Description, configuration, and algorithm version, the engine must always produce the same score.

### Reason

- Predictable behavior
- Easy debugging
- Easy benchmarking
- Reproducible results
- Easier regression testing

### Alternatives Considered

- LLM-generated scoring
- Probabilistic scoring

### Decision

Rejected.

LLMs may generate different scores for identical inputs.

---

# ADR-002

## AI Does Not Calculate ATS Score

### Decision

Artificial Intelligence will not directly calculate ATS scores.

### AI is permitted for

- Semantic similarity
- Embedding generation
- Evidence validation
- Future resume optimization

### AI is NOT permitted for

- Score calculation
- Weight calculation
- Final ATS decision

### Reason

ATS scores must remain deterministic.

---

# ADR-003

## Evidence First Architecture

### Decision

Every matched requirement must be supported by evidence.

### Examples

A skill may be supported by

- Experience
- Projects
- Certifications
- Resume Summary

### Reason

Prevents fake skill matching.

Improves explainability.

---

# ADR-004

## Single Evidence Generation

### Decision

Evidence is generated once.

Every downstream component reuses the same Evidence Object.

### Reason

Prevents

- Duplicate computation
- Conflicting evidence
- Different semantic interpretations

---

# ADR-005

## Shared Resume Quality Engine

### Decision

Resume Quality is implemented once.

It is reused by

- Resume Only
- Resume + JD

### Reason

- Consistent scoring
- Easier maintenance
- Single calibration process

---

# ADR-006

## Hybrid Matching Strategy

### Decision

Matching follows this order.

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

### Reason

Higher-confidence methods should always execute before lower-confidence methods.

---

# ADR-007

## Ontology Strategy

### Decision

Use a hybrid knowledge model.

Components

- Alias Dictionary
- Technology Ontology
- Embedding Model

### Reason

A static ontology alone becomes outdated.

Embeddings alone are difficult to explain.

The hybrid approach balances explainability and flexibility.

---

# ADR-008

## Semantic Matching

### Decision

Semantic matching is used only to validate evidence.

It is not a standalone scoring pillar.

### Reason

Avoids double-counting semantic information.

Keeps scoring explainable.

---

# ADR-009

## Integrity Engine

### Decision

Integrity violations reduce the ATS score.

### Examples

- Keyword Stuffing
- Hidden Text
- Fake Skills
- Unsupported Skills

### Rules

- Penalty is configurable.
- Penalty is capped.
- Final score is clamped between 0 and 100.
- Blocking violations may invalidate a submission.

### Reason

Discourages score manipulation.

---

# ADR-010

## Confidence

### Decision

Confidence never changes the ATS score.

Confidence measures the reliability of the evidence supporting the score.

### Types

- Overall Confidence
- Section Confidence
- Requirement Confidence

### Reason

Separates score from certainty.

---

# ADR-011

## Version-Controlled Scoring

### Decision

Every score must include version metadata.

### Metadata

- Algorithm Version
- Weight Version
- Rule Version
- Knowledge Version
- Ontology Version
- Embedding Model Version
- Calibration Dataset Version

### Reason

Ensures reproducibility.

---

# ADR-012

## Separation of Responsibilities

### Decision

Each engine owns exactly one responsibility.

Examples

- Parser → Parsing
- Entity Extraction → Entity Discovery
- Feature Engineering → Derived Features
- Matching Engine → Requirement Matching
- Integrity Engine → Anti-Gaming
- Output Engine → API Response

### Reason

Improves maintainability.

---

# ADR-013

## Explainability

### Decision

Every ATS score must be explainable.

The system must be able to answer

- Why was this skill matched?
- Why was it not matched?
- Why was a penalty applied?
- Why was the final score produced?

### Reason

Improves transparency.

Supports debugging.

Builds user trust.

---

# ADR-014

## Benchmark-Driven Calibration

### Decision

Scoring weights are calibrated using benchmark datasets.

Competitor scores are used only for directional comparison.

### Reason

Commercial ATS vendors do not publish their algorithms.

Calibration should rely on empirical validation rather than imitation.

---

# End of Architecture Decision Records