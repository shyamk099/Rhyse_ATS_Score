# ATS Resume Intelligence Engine

# Matching Confidence

**Version:** 1.0

---

# Purpose

The Matching Confidence Engine measures the reliability of every successful Resume ↔ Job Description match.

Matching Confidence represents how confidently the Hybrid Knowledge Layer determined that two features match.

Matching Confidence never modifies the ATS Score.

---

# Objectives

The Matching Confidence Engine must

- Measure match reliability.
- Preserve confidence throughout the pipeline.
- Produce deterministic confidence values.
- Support explainable matching.

---

# Scope

This module covers

- Exact Match Confidence
- Alias Match Confidence
- Fuzzy Match Confidence
- Ontology Match Confidence
- Semantic Match Confidence
- Overall Match Confidence

This module does not cover

- ATS Scoring
- Evidence Confidence
- Feature Confidence
- Entity Confidence

---

# Inputs

Consumes

- Match Object
- Matching Strategy
- Feature Confidence

Produced by

- Matching Pipeline

---

# Outputs

Produces

- Matching Confidence

Consumed by

- Evidence Intelligence
- Confidence Aggregator

---

# Processing Pipeline

```
Successful Match

↓

Strategy Validation

↓

Strategy Confidence

↓

Feature Confidence

↓

Overall Match Confidence

↓

Updated Match Object
```

---

# Confidence Philosophy

Matching Confidence answers one question.

> "How reliable is this match?"

It does not answer

> "How valuable is this match?"

Business value is determined later during ATS Scoring.

---

# Confidence Components

Every Match Object contains

## Strategy Confidence

Confidence contributed by the matching strategy.

---

## Feature Confidence

Confidence inherited from the matched features.

---

## Overall Match Confidence

Final confidence assigned to the Match Object.

---

# Strategy Confidence

Each matching strategy defines its own confidence model.

## Exact Matching

Highest confidence.

No interpretation required.

---

## Alias Matching

High confidence.

Based on canonical dictionary mappings.

---

## Fuzzy Matching

Confidence depends on

- Similarity Score
- Threshold Margin

---

## Ontology Matching

Confidence depends on

- Relationship Type
- Traversal Distance
- Relationship Validity

---

## Semantic Matching

Confidence depends on

- Embedding Similarity
- Threshold Margin
- Business Validation

---

# Confidence Rules

## Rule 1

Matching Confidence must always be deterministic.

---

## Rule 2

Matching Confidence never changes Match Objects.

Only confidence metadata is added.

---

## Rule 3

Matching Confidence never modifies ATS Score.

---

## Rule 4

Confidence calculations must be reproducible.

---

## Rule 5

Every Match Object stores its confidence.

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

# Validation

Validate

- Missing Match Objects
- Invalid Strategy
- Invalid Confidence Values
- Missing Feature Confidence

Return validation failures only.

---

# Match Confidence Object

```json
{
    "strategy_confidence": 0.0,
    "feature_confidence": 0.0,
    "overall_confidence": 0.0,
    "confidence_level": "",
    "confidence_reason": ""
}
```

---

# Example

```json
{
    "matching_strategy": "Ontology",
    "confidence": {
        "strategy_confidence": 96.5,
        "feature_confidence": 98.2,
        "overall_confidence": 97.4,
        "confidence_level": "Very High",
        "confidence_reason": "Direct ontology relationship with validated canonical entities."
    }
}
```

---

# Rules

## Rule 1

Matching Confidence is independent of ATS Score.

---

## Rule 2

Matching Confidence is preserved throughout the pipeline.

---

## Rule 3

Matching Confidence is immutable after creation.

---

## Rule 4

Every successful Match Object must contain confidence metadata.

---

# Dependencies

Consumes

- Match Object
- Feature Confidence

Produces

- Match Confidence

Consumed by

- Evidence Intelligence
- Confidence Aggregator

---

# Related Files

- Book_05_Hybrid_Knowledge_Layer.md
- Matching_Pipeline.md
- Match_JSON_Specification.md
- Exact_Matching.md
- Alias_Matching.md
- Fuzzy_Matching.md
- Ontology_Matching.md
- Semantic_Matching.md

---

# End of Matching Confidence