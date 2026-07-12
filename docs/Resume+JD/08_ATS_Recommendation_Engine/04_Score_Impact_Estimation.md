# ATS Resume Intelligence Engine

# Score Impact Estimation

**Version:** 1.0

---

# Purpose

The Score Impact Estimation Engine predicts the potential ATS score improvement that may result from implementing individual recommendations.

Its responsibility is to estimate score impact using existing scoring intelligence.

It never recalculates ATS scores.

It never guarantees future scores.

---

# Objectives

The Score Impact Estimation Engine must

- Estimate score improvement.
- Estimate score ranges.
- Estimate recommendation value.
- Preserve explainability.
- Produce deterministic estimations.

---

# Scope

This module covers

- Estimated Score Gain
- Predicted Score Range
- Impact Confidence
- Recommendation Value
- Aggregate Impact Estimation

This module does not cover

- ATS Scoring
- Resume Rewriting
- Resume Matching
- Recommendation Generation

---

# Inputs

Consumes

- Prioritized Recommendations
- Gap Objects
- Score JSON
- Evidence JSON

Produced by

- Recommendation Prioritization
- Gap Analysis
- ATS Scoring
- Evidence Intelligence

---

# Outputs

Produces

- Score Impact Estimates

Consumed by

- Recommendation Validation
- Recommendation JSON
- Recommendation API

---

# Processing Pipeline

```
Prioritized Recommendations

↓

Impact Analysis

↓

Estimated Score Gain

↓

Confidence Estimation

↓

Predicted Score Range

↓

Impact Object
```

---

# Design Philosophy

The Score Impact Estimation Engine answers one question.

> "If this recommendation is implemented, how much could the ATS score improve?"

The result is always an estimate.

It is never a guarantee.

The actual score is determined only after the Resume is re-evaluated by the ATS engine.

---

# Impact Components

Each recommendation receives

- Estimated Score Gain
- Predicted Score Range
- Impact Confidence
- Business Value
- Supporting Evidence

---

# Estimated Score Gain

Represents the expected improvement in ATS score.

Example

```
Current Score

74

↓

Estimated Gain

+4

↓

Predicted

78
```

---

# Predicted Score Range

Because recommendations interact with each other, the engine predicts a range instead of a single value.

Example

```
Current Score

74

↓

Predicted Score

77–79
```

---

# Impact Confidence

Each estimate includes a confidence level.

- Very High
- High
- Medium
- Low

Confidence reflects the reliability of the estimate, not the ATS score.

---

# Business Value

Measures how valuable the recommendation is from a hiring perspective.

Examples

- Critical Requirement
- Preferred Requirement
- Resume Quality Improvement
- ATS Compatibility Improvement

---

# Aggregate Impact

When multiple recommendations are selected together, the engine estimates their combined impact.

The combined estimate considers overlapping effects.

Individual estimates must not simply be summed.

---

# Estimation Rules

## Rule 1

Impact estimation never recalculates ATS scores.

---

## Rule 2

Impact estimation never guarantees score improvement.

---

## Rule 3

Every estimate must reference supporting Recommendation Objects.

---

## Rule 4

Impact estimation must be deterministic.

---

## Rule 5

Score ranges must remain within valid ATS score boundaries.

---

## Rule 6

Aggregate impact must account for overlapping recommendations.

---

# Example

```
Recommendation

Add Apache Spark

↓

Estimated Gain

+3 to +5

↓

Confidence

High

↓

Predicted Score

77–79
```

---

Another Example

```
Recommendation

Improve Experience Bullets

↓

Estimated Gain

+1 to +2

↓

Confidence

Medium
```

---

# Validation

Validate

- Missing Recommendation References
- Invalid Score Ranges
- Invalid Confidence Levels
- Invalid Estimated Gains
- Duplicate Impact Objects

Return validation failures only.

---

# Impact Object

Every Impact Object contains

- Impact ID
- Recommendation ID
- Estimated Score Gain
- Predicted Score Range
- Impact Confidence
- Business Value
- Supporting Evidence
- Metadata

---

# Output

Produces

- Score Impact Objects
- Aggregate Impact Summary
- Estimated Score Range

---

# Dependencies

Consumes

- Prioritized Recommendations
- Gap Objects
- Score JSON
- Evidence JSON

Produces

- Score Impact Estimates

Consumed by

- Recommendation Validation
- Recommendation JSON
- Recommendation API

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- Gap_Analysis.md
- Recommendation_Generation.md
- Recommendation_Prioritization.md
- Recommendation_Validation.md
- Recommendation_JSON_Specification.md
- Recommendation_API_Contract.md

---

# End of Score Impact Estimation