# ATS Resume Intelligence Engine

# Evidence Confidence

**Version:** 1.0

---

# Purpose

The Evidence Confidence Engine measures the reliability of every Evidence Object produced by the Evidence Intelligence layer.

Evidence Confidence represents how trustworthy the supporting evidence is for a Resume ↔ Job Description match.

Evidence Confidence improves explainability.

Evidence Confidence never changes the ATS Score.

---

# Objectives

The Evidence Confidence Engine must

- Measure evidence reliability.
- Preserve explainability.
- Produce deterministic confidence values.
- Support downstream scoring.
- Support auditability.

---

# Scope

This module covers

- Requirement Evidence Confidence
- Section Evidence Confidence
- Aggregated Evidence Confidence
- Overall Evidence Confidence

This module does not cover

- ATS Scoring
- Matching
- Feature Engineering
- Resume Optimization

---

# Inputs

Consumes

- Validated Evidence
- Matching Confidence
- Feature Confidence
- Entity Confidence

Produced by

- Evidence Validation
- Hybrid Knowledge Layer
- Feature Engineering
- Entity Extraction

---

# Outputs

Produces

- Evidence Confidence

Consumed by

- Evidence Aggregation
- ATS Scoring
- Explainability Engine

---

# Processing Pipeline

```
Validated Evidence

↓

Matching Confidence

↓

Feature Confidence

↓

Entity Confidence

↓

Evidence Confidence Calculation

↓

Evidence Confidence

↓

Validated Evidence
```

---

# Confidence Philosophy

Evidence Confidence answers one question.

> "How trustworthy is this supporting evidence?"

It does not answer

> "How much should this evidence contribute to the ATS Score?"

Business importance is calculated later by the ATS Scoring Engine.

---

# Confidence Sources

Evidence Confidence is derived from

- Matching Confidence
- Feature Confidence
- Entity Confidence
- Validation Status
- Evidence Completeness

---

# Confidence Components

Every Evidence Object stores

## Matching Confidence

Inherited from

Book 05

---

## Feature Confidence

Inherited from

Book 04

---

## Entity Confidence

Inherited from

Book 03

---

## Validation Confidence

Determined during

Evidence Validation

---

## Overall Evidence Confidence

Final confidence assigned to the Evidence Object.

---

# Confidence Levels

| Confidence | Level |
|------------|--------|
| 95–100 | Very High |
| 85–94 | High |
| 70–84 | Medium |
| 50–69 | Low |
| Below 50 | Very Low |

---

# Example

```
Evidence

↓

Python Skill

↓

Matching Confidence

99%

↓

Feature Confidence

98%

↓

Entity Confidence

100%

↓

Validation

Passed

↓

Overall Evidence Confidence

99%
```

---

# Confidence Rules

## Rule 1

Evidence Confidence must always be deterministic.

---

## Rule 2

Evidence Confidence never modifies Evidence Objects.

Only confidence metadata is added.

---

## Rule 3

Evidence Confidence never changes ATS Score.

---

## Rule 4

Every Evidence Object stores exactly one Overall Evidence Confidence.

---

## Rule 5

Confidence values must be reproducible.

---

## Rule 6

Confidence values must remain immutable after creation.

---

# Validation

Validate

- Missing Matching Confidence
- Missing Feature Confidence
- Missing Entity Confidence
- Invalid Confidence Values
- Missing Validation Status

Return validation failures only.

---

# Confidence Object

```json
{
  "matching_confidence": 0.0,
  "feature_confidence": 0.0,
  "entity_confidence": 0.0,
  "validation_confidence": 0.0,
  "overall_confidence": 0.0,
  "confidence_level": "",
  "confidence_reason": ""
}
```

---

# Example

```json
{
  "evidence_id": "EVD-000245",
  "confidence": {
    "matching_confidence": 98.7,
    "feature_confidence": 99.1,
    "entity_confidence": 100.0,
    "validation_confidence": 100.0,
    "overall_confidence": 99.2,
    "confidence_level": "Very High",
    "confidence_reason": "Validated evidence supported by high-confidence entity, feature and match."
  }
}
```

---

# Confidence Chain

Evidence Confidence is part of the overall confidence architecture.

```
Parser Confidence

↓

Entity Confidence

↓

Feature Confidence

↓

Matching Confidence

↓

Evidence Confidence

↓

Overall Confidence
```

---

# Non-Functional Requirements

The Evidence Confidence Engine must be

- Deterministic
- Stateless
- Explainable
- Auditable
- Repeatable

---

# Dependencies

Consumes

- Validated Evidence
- Matching Confidence
- Feature Confidence
- Entity Confidence

Produces

- Evidence Confidence

Consumed by

- Evidence Aggregation
- ATS Scoring
- Explainability Engine

---

# Related Files

- Book_06_Evidence_Intelligence.md
- Evidence_Generation.md
- Requirement_Evidence.md
- Section_Evidence.md
- Evidence_Validation.md
- Evidence_Aggregation.md
- Explainability_Model.md
- Evidence_JSON_Specification.md

---

# End of Evidence Confidence