# ATS Resume Intelligence Engine

# Feature JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Feature JSON model used throughout the ATS Resume Intelligence Engine.

The Feature JSON serves as the contract between the Feature Engineering layer and all downstream intelligence modules.

Every calculated feature must conform to this specification.

---

# Design Principles

The Feature JSON follows these principles.

- Deterministic
- Immutable
- Explainable
- Traceable
- Version Controlled
- Extensible

---

# Processing Flow

```
Resume / JD

↓

Entity JSON

↓

Feature Engineering

↓

Primitive Features

↓

Derived Features

↓

Feature JSON

↓

Hybrid Knowledge Layer
```

---

# Feature Structure

Every feature follows the same structure.

```json
{
  "feature_id": "",
  "feature_name": "",
  "feature_category": "",
  "feature_type": "",
  "value": null,
  "unit": "",
  "dependencies": [],
  "source_entities": [],
  "confidence": {},
  "metadata": {}
}
```

---

# Feature Fields

## feature_id

Unique identifier.

Example

```
FEAT-000001
```

---

## feature_name

Examples

- Skill Count
- Total Years of Experience
- Career Progression
- Employment Stability
- Resume Completeness

---

## feature_category

Examples

- Experience
- Skills
- Projects
- Education
- Certifications
- Leadership
- Resume Quality
- Requirements

---

## feature_type

Allowed values

- Primitive
- Derived

---

## value

Calculated feature value.

Examples

```
12

----------------

7.5

----------------

High

----------------

True
```

The value type depends on the feature.

---

## unit

Optional.

Examples

```
Years

Months

Count

Percentage

Level
```

---

# Dependencies

Dependencies contain the feature identifiers used to calculate this feature.

Example

```json
[
    "FEAT-000101",
    "FEAT-000102"
]
```

---

# Source Entities

References the originating Entity IDs.

Example

```json
[
    "ENT-000201",
    "ENT-000245",
    "ENT-000312"
]
```

---

# Confidence

```json
{
    "calculation_confidence": 0.0,
    "confidence_level": "",
    "confidence_reason": ""
}
```

---

# Metadata

```json
{
    "schema_version": "1.0",
    "formula_id": "",
    "engine_version": "",
    "timestamp": ""
}
```

---

# Example

```json
{
    "feature_id": "FEAT-000010",
    "feature_name": "Total Years of Experience",
    "feature_category": "Experience",
    "feature_type": "Derived",
    "value": 7.8,
    "unit": "Years",
    "dependencies": [
        "FEAT-000001",
        "FEAT-000002"
    ],
    "source_entities": [
        "ENT-000121",
        "ENT-000122",
        "ENT-000123"
    ],
    "confidence": {
        "calculation_confidence": 99.1,
        "confidence_level": "Very High",
        "confidence_reason": "Complete employment history."
    },
    "metadata": {
        "schema_version": "1.0",
        "formula_id": "FORM-EXP-001",
        "engine_version": "1.0"
    }
}
```

---

# Validation Rules

Validate

- Duplicate Feature IDs
- Invalid Feature Types
- Missing Values
- Missing Dependencies
- Invalid Entity References
- Invalid Confidence Values

Return validation errors only.

---

# Ownership

Only the Feature Engineering layer may create or modify Feature JSON.

Downstream engines consume Feature JSON but must never mutate it.

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

- Entity JSON

Produces

- Feature JSON

Consumed by

- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring
- Output API

---

# Related Files

- Book_04_Feature_Engineering.md
- Resume_Feature_Engineering.md
- JD_Feature_Engineering.md
- Derived_Features.md
- Feature_Calculation.md
- Feature_Confidence.md

---

# End of Feature JSON Specification