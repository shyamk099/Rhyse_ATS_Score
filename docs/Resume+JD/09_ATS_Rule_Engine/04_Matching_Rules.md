# ATS Resume Intelligence Engine

# Matching Rules

**Version:** 1.0

---

# Purpose

The Matching Rules Engine defines the configurable business rules used by the Resume–Job Description Matching Engine.

Matching Rules determine how Resume entities are compared against Job Description requirements.

Matching Rules never perform matching.

They only define how matching algorithms behave.

---

# Objectives

The Matching Rules Engine must

- Configure matching strategies.
- Configure matching weights.
- Configure similarity thresholds.
- Configure confidence thresholds.
- Configure match aggregation.
- Preserve deterministic matching.

---

# Scope

This module covers

- Exact Match Rules
- Alias Match Rules
- Ontology Match Rules
- Fuzzy Match Rules
- Semantic Match Rules
- Match Aggregation Rules
- Confidence Rules

This module does not cover

- Resume Parsing
- Entity Extraction
- Feature Engineering
- Match Calculation

---

# Inputs

Consumes

- Matching Rule Configuration

Produced by

- ATS Administrator
- Business Configuration

---

# Outputs

Produces

- Runtime Matching Rules

Consumed by

- Resume–JD Matching Engine

---

# Rule Philosophy

Matching Rules answer one question.

> "How should Resume requirements be matched against Job Description requirements?"

The Matching Engine executes the matching algorithms.

The Rule Engine only defines the matching policy.

---

# Processing Pipeline

```
Matching Rule Configuration

↓

Rule Loader

↓

Rule Validation

↓

Runtime Matching Rules

↓

Resume–JD Matching Engine
```

---

# Rule Categories

## Exact Match Rules

Defines

- Enable/Disable
- Weight
- Minimum Confidence

Example

```
Python

↓

Python

↓

Exact Match

Weight

1.00
```

---

## Alias Match Rules

Defines

- Enable/Disable
- Alias Dictionary
- Weight
- Confidence Threshold

Example

```
PySpark

↓

Apache Spark

↓

Alias Match
```

---

## Ontology Match Rules

Defines

- Enable/Disable
- Ontology Version
- Parent Matching
- Child Matching
- Weight

Example

```
Apache Spark

↓

Distributed Computing

↓

Ontology Match
```

---

## Fuzzy Match Rules

Defines

- Enable/Disable
- Similarity Algorithm
- Similarity Threshold
- Weight

Example

```
Tensor Flow

↓

TensorFlow

↓

Similarity

96%
```

---

## Semantic Match Rules

Defines

- Enable/Disable
- Embedding Model
- Similarity Threshold
- Weight

Example

```
ETL Development

↓

Data Pipeline Engineering

↓

Semantic Match
```

---

## Match Aggregation Rules

Defines

How multiple matching strategies are combined.

Supported strategies

- Highest Score
- Weighted Average
- Priority Order
- Best Evidence

Aggregation strategy is configurable.

---

## Confidence Rules

Defines

- Minimum Match Confidence
- Acceptance Threshold
- Manual Review Threshold

Example

```
Minimum Confidence

0.80
```

---

# Match Strategy Priority

Matching strategies are evaluated in order.

1. Exact Match
2. Alias Match
3. Ontology Match
4. Fuzzy Match
5. Semantic Match

Priority order is configurable.

---

# Rule Lifecycle

```
Configuration

↓

Validation

↓

Activation

↓

Matching Engine
```

---

# Rule Validation

Validate

- Missing Strategies
- Duplicate Strategies
- Invalid Weights
- Invalid Similarity Thresholds
- Invalid Confidence Values
- Invalid Aggregation Strategy

Only validated rules become active.

---

# Design Principles

## Configurable

Matching behavior must never be hardcoded.

---

## Deterministic

The same Resume and Job Description with the same rules must always produce identical Match Objects.

---

## Versioned

Every Matching Rule set has a version.

---

## Immutable

Rules cannot change during execution.

---

## Traceable

Every Match Object records the Matching Rule Version.

---

# Example Configuration

```yaml
matching:

  priority:
    - exact
    - alias
    - ontology
    - fuzzy
    - semantic

  exact:
    enabled: true
    weight: 1.00

  alias:
    enabled: true
    weight: 0.95

  ontology:
    enabled: true
    weight: 0.90

  fuzzy:
    enabled: true
    threshold: 0.90
    weight: 0.85

  semantic:
    enabled: true
    embedding_model: BGE-v1.5
    threshold: 0.82
    weight: 0.75

  aggregation:
    strategy: weighted_average

  confidence:
    minimum: 0.80
```

---

# Rule Rules

## Rule 1

Matching strategies must be configurable.

---

## Rule 2

Weights must never be hardcoded.

---

## Rule 3

Rules are read-only during execution.

---

## Rule 4

Invalid Matching Rules must never be activated.

---

## Rule 5

Every Match Object records the Matching Rule Version.

---

## Rule 6

Runtime engines cannot modify Matching Rules.

---

# Dependencies

Consumes

- Matching Rule Configuration

Produces

- Runtime Matching Rules

Consumed by

- Resume–JD Matching Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- Parser_Rules.md
- Entity_Rules.md
- Feature_Rules.md
- Evidence_Rules.md
- Scoring_Rules.md
- Recommendation_Rules.md
- Rule_JSON_Specification.md

---

# End of Matching Rules