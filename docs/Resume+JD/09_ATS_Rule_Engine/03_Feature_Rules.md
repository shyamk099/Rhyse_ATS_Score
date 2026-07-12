# ATS Resume Intelligence Engine

# Feature Rules

**Version:** 1.0

---

# Purpose

The Feature Rules Engine defines the configurable business rules used by the Feature Engineering Engine.

Feature Rules determine how Resume Features are calculated, aggregated, validated, and normalized.

Feature Rules never calculate features.

They only define how feature calculations should behave.

---

# Objectives

The Feature Rules Engine must

- Configure feature calculations.
- Configure aggregation policies.
- Configure normalization rules.
- Configure validation thresholds.
- Preserve deterministic feature generation.

---

# Scope

This module covers

- Skill Feature Rules
- Experience Feature Rules
- Project Feature Rules
- Education Feature Rules
- Certification Feature Rules
- Aggregation Rules
- Normalization Rules

This module does not cover

- Resume Parsing
- Entity Extraction
- Feature Calculation

---

# Inputs

Consumes

- Feature Rule Configuration

Produced by

- ATS Administrator
- Business Configuration

---

# Outputs

Produces

- Runtime Feature Rules

Consumed by

- Feature Engineering Engine

---

# Rule Philosophy

Feature Rules answer one question.

> "How should Resume Features be calculated?"

Feature calculations are executed by the Feature Engineering Engine.

The Rule Engine defines only the business policy.

---

# Processing Pipeline

```
Feature Rule Configuration

↓

Rule Loader

↓

Rule Validation

↓

Runtime Feature Rules

↓

Feature Engineering Engine
```

---

# Rule Categories

## Skill Feature Rules

Defines

- Skill Weight
- Skill Frequency
- Skill Density
- Skill Confidence
- Skill Importance

Example

```
Apache Spark

Weight

10
```

---

## Experience Feature Rules

Defines

- Minimum Experience
- Maximum Experience
- Experience Scaling
- Leadership Threshold
- Domain Experience

Example

```
Years Experience

Minimum

2

Maximum

40
```

---

## Project Feature Rules

Defines

- Project Importance
- Project Complexity
- Project Relevance
- Technical Diversity

---

## Education Feature Rules

Defines

- Degree Ranking
- Education Weight
- Institution Weight
- GPA Rules

---

## Certification Feature Rules

Defines

- Certification Priority
- Expiration Rules
- Certification Categories

---

## Aggregation Rules

Defines how multiple features are combined.

Examples

- Average
- Maximum
- Weighted Average
- Sum

Aggregation strategy is configurable.

---

## Normalization Rules

Defines

- Feature Scaling
- Feature Bounds
- Default Values
- Missing Feature Handling

Example

```
Feature Range

0

↓

100
```

---

# Rule Lifecycle

```
Configuration

↓

Validation

↓

Activation

↓

Feature Engineering
```

---

# Rule Validation

Validate

- Missing Rules
- Duplicate Rules
- Invalid Weights
- Invalid Thresholds
- Invalid Aggregation Strategies
- Invalid Feature Bounds

Only validated rules become active.

---

# Design Principles

## Configurable

Feature calculations must never be hardcoded.

---

## Deterministic

The same Resume with the same rules must always produce identical features.

---

## Versioned

Every Feature Rule set has a version.

---

## Immutable

Rules cannot change during execution.

---

## Traceable

Every generated Feature records the Feature Rule Version.

---

# Example Configuration

```yaml
feature:

  skill:

    default_weight: 5

    important_skills:

      apache_spark:
        weight: 10

      python:
        weight: 9

      aws:
        weight: 8

  experience:

    minimum_years: 2

    maximum_years: 40

  aggregation:

    strategy: weighted_average

  normalization:

    minimum: 0

    maximum: 100
```

---

# Rule Rules

## Rule 1

Feature calculations must be configurable.

---

## Rule 2

Rules are read-only during execution.

---

## Rule 3

Invalid rule sets must never be activated.

---

## Rule 4

Every Feature calculation records the Rule Version.

---

## Rule 5

Runtime engines cannot modify Feature Rules.

---

# Dependencies

Consumes

- Feature Rule Configuration

Produces

- Runtime Feature Rules

Consumed by

- Feature Engineering Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- Parser_Rules.md
- Entity_Rules.md
- Matching_Rules.md
- Rule_JSON_Specification.md

---

# End of Feature Rules