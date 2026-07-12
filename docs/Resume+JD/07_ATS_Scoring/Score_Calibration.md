# ATS Resume Intelligence Engine

# Score Calibration

**Version:** 1.0

---

# Purpose

The Score Calibration Engine transforms the Raw ATS Score into the Final ATS Score.

Its responsibility is to normalize scores, maintain consistency across algorithm versions, and ensure fair comparison between Resume evaluations.

The Score Calibration Engine never recalculates component scores.

---

# Objectives

The Score Calibration Engine must

- Normalize Raw ATS Scores.
- Maintain score consistency.
- Preserve historical comparability.
- Apply calibration rules.
- Produce the Final ATS Score.

---

# Scope

This module covers

- Score Normalization
- Calibration Rules
- Score Bounds
- Version Calibration
- Final Score Generation

This module does not cover

- Resume Parsing
- Resume Matching
- Evidence Generation
- Component Score Calculation
- Weight Calculation

---

# Inputs

Consumes

- Raw ATS Score

Produced by

- Weighted Scoring Engine

---

# Outputs

Produces

- Final ATS Score

Consumed by

- Score JSON
- Output API
- Analytics Engine

---

# Design Philosophy

The Score Calibration Engine answers one question.

> "How do we ensure ATS Scores remain fair, stable, and comparable?"

Calibration never changes Resume intelligence.

Calibration only transforms the Raw Score into the Final ATS Score.

---

# Processing Pipeline

```
Raw ATS Score

↓

Score Validation

↓

Calibration Rules

↓

Score Normalization

↓

Boundary Validation

↓

Final ATS Score
```

---

# Calibration Components

The Score Calibration Engine performs

- Raw Score Validation
- Score Normalization
- Boundary Validation
- Version Calibration
- Final Score Validation

---

# Score Normalization

Normalization ensures

- Final Score remains between configured limits.
- Scores remain comparable.
- Minor algorithm improvements do not create large score shifts.

---

# Score Boundaries

The Final ATS Score must remain within

```
Minimum Score

0

↓

Maximum Score

100
```

Any value outside these limits is normalized.

---

# Version Calibration

Calibration supports

- Algorithm Version
- Weight Version
- Calibration Version

Historical scores remain comparable even after algorithm improvements.

---

# Calibration Rules

## Rule 1

Calibration never recalculates component scores.

---

## Rule 2

Calibration never changes supporting evidence.

---

## Rule 3

Calibration never changes Match Objects.

---

## Rule 4

Calibration must be deterministic.

---

## Rule 5

Calibration rules are version controlled.

---

## Rule 6

Every Final ATS Score must be reproducible.

---

# Validation

Validate

- Invalid Raw Score
- Missing Calibration Version
- Invalid Score Range
- Missing Weight Version
- Invalid Algorithm Version

Return validation failures only.

---

# Example

```
Raw ATS Score

84.6

↓

Calibration

↓

Final ATS Score

85
```

---

Another Example

```
Raw ATS Score

102

↓

Normalization

↓

Final ATS Score

100
```

---

# Calibration Metadata

Every calibrated score records

- Calibration Version
- Algorithm Version
- Weight Version
- Timestamp

---

# Output

Produces

- Final ATS Score
- Calibration Summary
- Calibration Metadata

---

# Dependencies

Consumes

- Raw ATS Score

Produces

- Final ATS Score

Consumed by

- Score_JSON_Specification.md
- ATS_Final_Score.md
- Output API

---

# Related Files

- Book_07_ATS_Scoring.md
- Weighted_Scoring_Engine.md
- Score_Versioning.md
- Score_JSON_Specification.md
- ATS_Final_Score.md

---

# End of Score Calibration