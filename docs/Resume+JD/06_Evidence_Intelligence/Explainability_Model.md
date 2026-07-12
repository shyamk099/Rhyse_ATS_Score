# ATS Resume Intelligence Engine

# Explainability Model

**Version:** 1.0

---

# Purpose

The Explainability Model transforms technical Evidence Objects into human-readable explanations.

Its responsibility is to explain every ATS decision in a transparent, traceable, and deterministic manner.

The Explainability Model does not perform Resume matching, Evidence generation, or ATS scoring.

It only explains the intelligence already produced by previous layers.

---

# Objectives

The Explainability Model must

- Explain ATS decisions.
- Explain Requirement coverage.
- Explain Resume strengths.
- Explain Resume weaknesses.
- Generate deterministic explanations.
- Preserve complete traceability.

---

# Scope

This module covers

- Match Explanation
- Requirement Explanation
- Section Explanation
- Score Explanation
- Missing Requirement Explanation
- Strength Explanation
- Weakness Explanation

This module does not cover

- Resume Matching
- Evidence Generation
- ATS Scoring
- Resume Optimization

---

# Inputs

Consumes

- Aggregated Evidence
- Requirement Evidence
- Section Evidence
- Evidence Confidence

Produced by

- Evidence Aggregation
- Requirement Evidence
- Section Evidence
- Evidence Confidence

---

# Outputs

Produces

- Explainability Objects

Consumed by

- Output API
- ATS Report Generator
- Resume Optimization Engine

---

# Processing Pipeline

```
Aggregated Evidence

↓

Requirement Analysis

↓

Section Analysis

↓

Strength Analysis

↓

Weakness Analysis

↓

Explanation Generation

↓

Explainability Object
```

---

# Explainability Philosophy

Every ATS decision must be explainable.

The system should always answer

- What matched?
- Why did it match?
- Which Resume section supports it?
- Which JD requirement supports it?
- Which matching strategy was used?
- How confident is the evidence?
- Why did this affect the ATS score?

---

# Explanation Categories

## Requirement Explanation

Explains

- Requirement matched
- Requirement partially matched
- Requirement missing

---

## Section Explanation

Explains

- Experience contribution
- Skills contribution
- Project contribution
- Education contribution
- Certification contribution

---

## Strength Explanation

Identifies Resume strengths.

Examples

- Strong Python experience.
- Excellent cloud expertise.
- Multiple relevant projects.
- High requirement coverage.

---

## Weakness Explanation

Identifies Resume weaknesses.

Examples

- Missing Kubernetes experience.
- No cloud certification.
- Limited leadership evidence.
- Missing required skills.

---

## Match Explanation

Explains

- Matching strategy used.
- Evidence supporting the match.
- Confidence level.

Example

```
Requirement

Python

↓

Matched

↓

Strategy

Exact Match

↓

Evidence

Python listed in Skills section.

↓

Confidence

Very High
```

---

## Coverage Explanation

Explains

- Requirement Coverage
- Resume Coverage
- Section Coverage

Example

```
Required Skills

10

↓

Matched

8

↓

Coverage

80%
```

---

# Explanation Structure

Each explanation contains

- Explanation ID
- Explanation Type
- Related Requirement
- Related Resume Section
- Supporting Evidence IDs
- Confidence
- Human-readable Explanation

---

# Explanation Rules

## Rule 1

Every explanation must reference valid Evidence Objects.

---

## Rule 2

Every explanation must be deterministic.

---

## Rule 3

No explanation may invent information.

---

## Rule 4

No explanation may modify Evidence Objects.

---

## Rule 5

Every explanation must preserve traceability.

---

## Rule 6

Every explanation must be human-readable.

---

## Rule 7

Confidence displayed must originate from Evidence Confidence.

---

# Validation

Validate

- Missing Evidence References
- Missing Requirement References
- Invalid Resume Sections
- Empty Explanations
- Missing Confidence

Return validation failures only.

---

# Explainability Object

Each Explainability Object contains

- Explanation ID
- Explanation Type
- Requirement Reference
- Resume Section Reference
- Supporting Evidence IDs
- Explanation Text
- Confidence
- Metadata

---

# Example

```
Requirement

AWS

↓

Status

Matched

↓

Evidence

AWS listed in Skills
AWS Project
AWS Experience

↓

Explanation

"The Resume demonstrates strong AWS experience through multiple supporting sections."

↓

Confidence

Very High
```

---

# Non-Functional Requirements

The Explainability Model must be

- Deterministic
- Explainable
- Stateless
- Auditable
- Traceable

---

# Dependencies

Consumes

- Aggregated Evidence
- Requirement Evidence
- Section Evidence
- Evidence Confidence

Produces

- Explainability Objects

Consumed by

- Output API
- ATS Report Generator
- Resume Optimization Engine

---

# Related Files

- Book_06_Evidence_Intelligence.md
- Evidence_Generation.md
- Requirement_Evidence.md
- Section_Evidence.md
- Evidence_Validation.md
- Evidence_Confidence.md
- Evidence_Aggregation.md
- Evidence_JSON_Specification.md

---

# End of Explainability Model