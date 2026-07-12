# ATS Resume Intelligence Engine

# Match JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Match JSON model used throughout the ATS Resume Intelligence Engine.

The Match JSON serves as the contract between the Hybrid Knowledge Layer and all downstream intelligence modules.

Every successful Resume ↔ Job Description comparison produces a Match Object that conforms to this specification.

---

# Design Principles

The Match JSON follows these principles.

- Deterministic
- Immutable
- Explainable
- Traceable
- Version Controlled
- Extensible

---

# Processing Flow

```
Resume Feature JSON

+

JD Feature JSON

↓

Matching Pipeline

↓

Matching Strategy

↓

Matching Confidence

↓

Match JSON

↓

Evidence Intelligence
```

---

# Match Structure

Every successful match follows the same structure.

```json
{
    "match_id": "",
    "resume_feature_id": "",
    "jd_feature_id": "",
    "matching_strategy": "",
    "match_status": "",
    "match_reason": "",
    "relationship": {},
    "similarity": {},
    "confidence": {},
    "metadata": {}
}
```

---

# Match Fields

## match_id

Unique identifier.

Example

```
MATCH-000001
```

---

## resume_feature_id

Reference to the Resume Feature.

Example

```
FEAT-R-001245
```

---

## jd_feature_id

Reference to the Job Description Feature.

Example

```
FEAT-J-000532
```

---

## matching_strategy

Allowed values

- Exact
- Alias
- Fuzzy
- Ontology
- Semantic

Only one strategy is permitted.

---

## match_status

Allowed values

- Matched
- Not Matched

---

## match_reason

Human-readable explanation.

Examples

```
Exact canonical value match.
```

```
Matched through official alias.
```

```
Matched through ontology relationship.
```

```
Matched using semantic similarity.
```

---

# Relationship Object

Only populated for Ontology Matching.

```json
{
    "relationship_type": "",
    "source_node": "",
    "target_node": "",
    "traversal_depth": 0
}
```

Otherwise

```json
null
```

---

# Similarity Object

Used when applicable.

```json
{
    "similarity_score": 0.0,
    "threshold": 0.0
}
```

Examples

- Fuzzy Matching
- Semantic Matching

Exact and Alias Matching may leave this object empty.

---

# Confidence Object

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

# Metadata

```json
{
    "pipeline_version": "",
    "algorithm_version": "",
    "ontology_version": "",
    "alias_dictionary_version": "",
    "embedding_model_version": "",
    "timestamp": ""
}
```

Only the relevant version fields are populated.

Example

Exact Match

```
Algorithm Version
```

Ontology Match

```
Algorithm Version

Ontology Version
```

Semantic Match

```
Algorithm Version

Embedding Model Version
```

---

# Example

```json
{
    "match_id": "MATCH-000145",
    "resume_feature_id": "FEAT-R-000421",
    "jd_feature_id": "FEAT-J-000188",
    "matching_strategy": "Ontology",
    "match_status": "Matched",
    "match_reason": "Amazon EMR is a managed service running on AWS.",
    "relationship": {
        "relationship_type": "runs_on",
        "source_node": "Amazon EMR",
        "target_node": "AWS",
        "traversal_depth": 1
    },
    "similarity": null,
    "confidence": {
        "strategy_confidence": 96.8,
        "feature_confidence": 98.5,
        "overall_confidence": 97.6,
        "confidence_level": "Very High",
        "confidence_reason": "Direct ontology relationship."
    },
    "metadata": {
        "pipeline_version": "1.0",
        "algorithm_version": "1.0",
        "ontology_version": "1.2"
    }
}
```

---

# Validation Rules

Validate

- Duplicate Match IDs
- Missing Feature References
- Invalid Matching Strategy
- Invalid Confidence Values
- Invalid Relationship Object
- Invalid Similarity Object

Return validation failures only.

---

# Ownership

Only the Hybrid Knowledge Layer may create or modify Match JSON.

Downstream engines consume Match JSON but must never mutate it.

---

# Schema Evolution

Rules

- Never remove fields in minor versions.
- New fields must remain optional until the next major version.
- Breaking changes require a schema version increment.
- Schema updates must be documented before implementation.

---

# Dependencies

Consumes

- Resume Feature JSON
- JD Feature JSON

Produces

- Match JSON

Consumed by

- Evidence Intelligence
- ATS Scoring
- Output API

---

# Related Files

- Book_05_Hybrid_Knowledge_Layer.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Exact_Matching.md
- Alias_Matching.md
- Fuzzy_Matching.md
- Ontology_Matching.md
- Semantic_Matching.md

---

# End of Match JSON Specification