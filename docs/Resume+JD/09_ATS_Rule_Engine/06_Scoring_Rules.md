# ATS Resume Intelligence Engine

# Scoring Rules

**Version:** 1.0

---

# Purpose

The Scoring Rules Engine defines the configurable business rules used by the ATS Scoring Engine.

Scoring Rules determine how component scores are weighted, calibrated, validated, and combined into the Final ATS Score.

Scoring Rules never calculate ATS scores.

They only define the scoring policy.

---

# Objectives

The Scoring Rules Engine must

- Configure score weights.
- Configure score boundaries.
- Configure integrity penalties.
- Configure calibration rules.
- Configure score classifications.
- Preserve deterministic scoring.

---

# Scope

This module covers

- Component Weight Rules
- Score Boundary Rules
- Integrity Penalty Rules
- Calibration Rules
- Classification Rules
- Validation Rules

This module does not cover

- ATS Score Calculation
- Resume Matching
- Evidence Generation
- Recommendation Generation

---

# Inputs

Consumes

- Scoring Rule Configuration

Produced by

- ATS Administrator
- Business Configuration

---

# Outputs

Produces

- Runtime Scoring Rules

Consumed by

- ATS Scoring Engine

---

# Rule Philosophy

Scoring Rules answer one question.

> "How should ATS scores be calculated and interpreted?"

The ATS Scoring Engine performs calculations.

The Rule Engine defines the scoring policy.

---

# Processing Pipeline

```
Scoring Rule Configuration

↓

Rule Loader

↓

Rule Validation

↓

Runtime Scoring Rules

↓

ATS Scoring Engine
```

---

# Rule Categories

## Component Weight Rules

Defines the contribution of every scoring component.

Example

| Component | Weight |
|------------|---------|
| ATS Compatibility | 20% |
| Resume Quality | 20% |
| Resume–JD Match | 45% |
| Semantic Validation | 15% |

Weights are configurable.

---

## Integrity Penalty Rules

Defines

- Keyword Stuffing Penalty
- Duplicate Keyword Penalty
- Hidden Text Penalty
- Artificial Skill Inflation Penalty

Example

```
Keyword Stuffing

Penalty

5
```

Penalty values are configurable.

---

## Score Boundary Rules

Defines

- Minimum Score
- Maximum Score
- Minimum Component Score
- Maximum Component Score

Example

```
Minimum

0

Maximum

100
```

---

## Calibration Rules

Defines

- Calibration Enabled
- Calibration Method
- Score Adjustment Limits

Calibration strategy is configurable.

---

## Classification Rules

Defines score classifications.

Example

| Score | Grade |
|--------|--------|
| 90–100 | Outstanding |
| 80–89 | Excellent |
| 70–79 | Strong |
| 60–69 | Good |
| Below 60 | Needs Improvement |

Classification thresholds are configurable.

---

## Validation Rules

Defines

- Valid Weight Range
- Total Weight Validation
- Penalty Validation
- Calibration Validation

Only valid scoring configurations become active.

---

# Rule Lifecycle

```
Configuration

↓

Validation

↓

Activation

↓

ATS Scoring
```

---

# Rule Validation

Validate

- Missing Component Weights
- Invalid Weight Values
- Weight Total Not Equal to 100%
- Invalid Penalty Values
- Invalid Calibration Rules
- Invalid Classification Thresholds

Only validated rule sets become active.

---

# Design Principles

## Configurable

Scoring policy must never be hardcoded.

---

## Deterministic

The same inputs with the same scoring rules must always produce identical scores.

---

## Versioned

Every Scoring Rule set has a version.

---

## Immutable

Rules cannot change during execution.

---

## Traceable

Every ATS Score records the Scoring Rule Version.

---

# Example Configuration

```yaml
scoring:

  weights:

    ats_compatibility: 20

    resume_quality: 20

    resume_jd_match: 45

    semantic_validation: 15

  penalties:

    keyword_stuffing: 5

    hidden_text: 10

    duplicate_keywords: 3

  score_boundaries:

    minimum: 0

    maximum: 100

  calibration:

    enabled: true

    method: normalization

  classification:

    outstanding: 90

    excellent: 80

    strong: 70

    good: 60
```

---

# Rule Rules

## Rule 1

Component weights must total 100%.

---

## Rule 2

Penalty values must be configurable.

---

## Rule 3

Rules are read-only during execution.

---

## Rule 4

Invalid Scoring Rules must never be activated.

---

## Rule 5

Every ATS evaluation records the Scoring Rule Version.

---

## Rule 6

Runtime engines cannot modify Scoring Rules.

---

# Dependencies

Consumes

- Scoring Rule Configuration

Produces

- Runtime Scoring Rules

Consumed by

- ATS Scoring Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- Parser_Rules.md
- Entity_Rules.md
- Feature_Rules.md
- Matching_Rules.md
- Evidence_Rules.md
- Recommendation_Rules.md
- Rule_JSON_Specification.md

---

# End of Scoring Rules