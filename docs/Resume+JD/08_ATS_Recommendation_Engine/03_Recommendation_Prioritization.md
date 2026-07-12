# ATS Resume Intelligence Engine

# Recommendation Prioritization

**Version:** 1.0

---

# Purpose

The Recommendation Prioritization Engine ranks Recommendation Objects according to their expected business value and impact on the ATS Score.

Its responsibility is to determine the optimal execution order for Resume improvements.

The engine never modifies Recommendation content.

It only determines execution priority.

---

# Objectives

The Recommendation Prioritization Engine must

- Rank Recommendations.
- Estimate business importance.
- Estimate expected ATS score improvement.
- Produce deterministic priorities.
- Generate execution order.

---

# Scope

This module covers

- Priority Calculation
- Priority Ranking
- Recommendation Ordering
- Execution Sequencing

This module does not cover

- Recommendation Generation
- Resume Rewriting
- ATS Scoring
- Prompt Engineering

---

# Inputs

Consumes

- Recommendation Objects
- Gap Objects
- Evidence JSON
- Score JSON

Produced by

- Recommendation Generation
- Gap Analysis
- Evidence Intelligence
- ATS Scoring

---

# Outputs

Produces

- Prioritized Recommendations

Consumed by

- Score Impact Estimation
- Recommendation Validation
- Recommendation JSON

---

# Processing Pipeline

```
Recommendation Objects

↓

Business Importance

↓

Priority Score

↓

Ranking

↓

Execution Order

↓

Prioritized Recommendations
```

---

# Prioritization Philosophy

The Recommendation Prioritization Engine answers one question.

> "Which recommendation should be implemented first?"

Recommendations with the highest expected value appear first.

Priority is determined using measurable factors.

---

# Priority Components

Each Recommendation receives a Priority Score based on

- Business Importance
- Estimated Score Gain
- Requirement Criticality
- Coverage Improvement
- Evidence Strength
- Implementation Complexity

---

# Business Importance

Measures

- Mandatory Requirement
- Preferred Requirement
- Optional Requirement

Mandatory requirements receive higher priority.

---

# Estimated Score Gain

Measures

Expected improvement in ATS Score if the recommendation is implemented.

Higher gain results in higher priority.

---

# Requirement Criticality

Measures

How critical the requirement is to the Job Description.

Examples

- Required Skill
- Required Experience
- Required Certification

---

# Coverage Improvement

Measures

Expected increase in Requirement Coverage.

Example

```
Current Coverage

72%

↓

Expected

80%
```

---

# Evidence Strength

Recommendations supported by stronger evidence receive higher confidence and priority.

Weak or uncertain evidence reduces priority.

---

# Implementation Complexity

Measures

Estimated effort required to address the recommendation.

Examples

Low Complexity

- Improve Summary
- Remove Tables

High Complexity

- Gain 5 years of experience
- Obtain Certification

Complexity affects recommendation ordering only.

It never changes the ATS Score.

---

# Priority Score

Priority is calculated using configurable business rules.

Conceptually

```
Priority Score

=

Business Importance

+

Estimated Score Gain

+

Coverage Improvement

+

Evidence Strength

-

Implementation Complexity
```

The exact weighting is configurable.

---

# Priority Levels

Each Recommendation receives one priority.

- Critical
- High
- Medium
- Low

---

# Execution Order

Recommendations are sorted by

1. Priority Score
2. Business Importance
3. Estimated Score Gain
4. Coverage Improvement
5. Recommendation ID

This guarantees deterministic ordering.

---

# Example

```
Recommendation

Add Apache Spark

↓

Estimated Gain

+6

↓

Business Importance

Mandatory

↓

Priority

Critical
```

---

Another Example

```
Recommendation

Improve Summary

↓

Estimated Gain

+1

↓

Priority

Low
```

---

# Prioritization Rules

## Rule 1

Every Recommendation receives exactly one Priority Score.

---

## Rule 2

Priority calculation must always be deterministic.

---

## Rule 3

Recommendations never change category during prioritization.

---

## Rule 4

Prioritization never modifies Recommendation Objects.

---

## Rule 5

Priority Rules are version controlled.

---

## Rule 6

Execution order must always be reproducible.

---

# Validation

Validate

- Duplicate Priorities
- Invalid Priority Levels
- Missing Business Importance
- Missing Estimated Score Gain
- Missing Coverage Values

Return validation failures only.

---

# Output

Produces

- Prioritized Recommendations
- Priority Summary
- Execution Order

---

# Dependencies

Consumes

- Recommendation Objects
- Gap Objects
- Evidence JSON
- Score JSON

Produces

- Prioritized Recommendations

Consumed by

- Score Impact Estimation
- Recommendation Validation
- Recommendation JSON

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- Gap_Analysis.md
- Recommendation_Generation.md
- Score_Impact_Estimation.md
- Recommendation_Validation.md
- Recommendation_JSON_Specification.md
- Recommendation_API_Contract.md

---

# End of Recommendation Prioritization