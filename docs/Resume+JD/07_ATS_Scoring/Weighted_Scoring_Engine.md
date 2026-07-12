# ATS Resume Intelligence Engine

# Weighted Scoring Engine

**Version:** 1.0

---

# Purpose

The Weighted Scoring Engine combines all component scores into a single Raw ATS Score.

It is the orchestration layer of the ATS Scoring Engine.

The Weighted Scoring Engine never performs parsing, matching, evidence generation, semantic reasoning, or component score calculation.

Each component score is calculated independently before entering this engine.

---

# Objectives

The Weighted Scoring Engine must

- Combine component scores.
- Apply configurable weights.
- Apply Integrity Penalty.
- Produce Raw ATS Score.
- Preserve explainability.
- Produce deterministic results.

---

# Scope

This module covers

- Component Weighting
- Score Aggregation
- Raw Score Calculation
- Integrity Penalty Application
- Weight Validation

This module does not cover

- ATS Compatibility Calculation
- Resume Quality Calculation
- Resume–JD Matching
- Semantic Matching
- Score Calibration

---

# Inputs

Consumes

- ATS Compatibility Score
- Resume Quality Score
- Resume–JD Match Score
- Semantic Validation Score
- Integrity Penalty

Produced by

- ATS Compatibility Engine
- Resume Quality Engine
- Resume–JD Match Engine
- Semantic Validation Engine
- Integrity Penalty Engine

---

# Outputs

Produces

- Raw ATS Score

Consumed by

- Score Calibration

---

# Design Philosophy

The Weighted Scoring Engine answers one question.

> "How should the independently calculated scores be combined into one Raw ATS Score?"

It never decides

- how ATS Compatibility is calculated,
- how Resume Quality is calculated,
- how Resume–JD Match is calculated,
- how Semantic Validation is calculated.

Those responsibilities belong to their respective engines.

---

# Processing Pipeline

```
ATS Compatibility Score

+

Resume Quality Score

+

Resume–JD Match Score

+

Semantic Validation Score

↓

Weighted Aggregation

↓

Integrity Penalty

↓

Raw ATS Score
```

---

# Raw Score Formula

```
Raw ATS Score

=

(ATS Compatibility Score × ATS Weight)

+

(Resume Quality Score × Resume Weight)

+

(Resume–JD Match Score × Match Weight)

+

(Semantic Validation Score × Semantic Weight)

-

Integrity Penalty
```

---

# Weight Configuration

Every scoring component has a configurable weight.

Example

| Component | Weight |
|-----------|--------|
| ATS Compatibility | Configurable |
| Resume Quality | Configurable |
| Resume–JD Match | Configurable |
| Semantic Validation | Configurable |

Weights are not hardcoded.

Weights are loaded from the Scoring Configuration.

---

# Weight Rules

## Rule 1

All weights are version controlled.

---

## Rule 2

The total positive weight must equal 100%.

---

## Rule 3

Negative weights are not permitted.

---

## Rule 4

Weights may only change through a new Weight Version.

---

## Rule 5

Integrity Penalty is never weighted.

It is applied after weighted aggregation.

---

# Score Validation

Validate

- Missing Component Scores
- Invalid Weight Values
- Invalid Total Weight
- Missing Integrity Penalty
- Invalid Raw Score

Return validation failures only.

---

# Explainability

Every Raw ATS Score records

- Component Scores
- Applied Weights
- Integrity Penalty
- Raw Score Calculation

Every calculation must be reproducible.

---

# Example

```
ATS Compatibility

92

↓

Resume Quality

90

↓

Resume–JD Match

84

↓

Semantic Validation

88

↓

Weighted Aggregation

↓

87.6

↓

Integrity Penalty

3

↓

Raw ATS Score

84.6
```

---

# Weight Version

Every calculation records

- Weight Version
- Algorithm Version
- Calculation Timestamp

This guarantees reproducibility.

---

# Rules

## Rule 1

Component scores are immutable.

---

## Rule 2

Weights are immutable during execution.

---

## Rule 3

The engine never recalculates component scores.

---

## Rule 4

Integrity Penalty is applied exactly once.

---

## Rule 5

Raw ATS Score must always be deterministic.

---

## Rule 6

Every calculation must be fully traceable.

---

# Dependencies

Consumes

- Component Scores
- Integrity Penalty

Produces

- Raw ATS Score

Consumed by

- Score Calibration

---

# Related Files

- Book_07_ATS_Scoring.md
- ATS_Compatibility_Score.md
- Resume_Quality_Score.md
- Resume_JD_Match_Score.md
- Semantic_Validation_Score.md
- Integrity_Penalty.md
- Score_Calibration.md
- Score_Versioning.md
- Score_JSON_Specification.md

---

# End of Weighted Scoring Engine