# ATS Resume Intelligence Engine

# Rule JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Rule JSON model used throughout the ATS Resume Intelligence Engine.

Rule JSON is the official configuration contract consumed by every ATS engine.

It centralizes all configurable business policies while keeping the intelligence engines generic and deterministic.

Rule JSON is immutable once activated.

---

# Design Principles

Rule JSON follows these principles.

- Deterministic
- Versioned
- Immutable
- Auditable
- Traceable
- Extensible

---

# Processing Flow

```
Rule JSON

↓

Rule Loader

↓

Rule Validation

↓

Runtime Rule Objects

↓

Parser

↓

Entity

↓

Feature

↓

Matching

↓

Evidence

↓

Scoring

↓

Recommendation
```

---

# Rule JSON Structure

```json
{
    "metadata": {},
    "parser": {},
    "entity": {},
    "feature": {},
    "matching": {},
    "evidence": {},
    "scoring": {},
    "recommendation": {}
}
```

---

# Metadata

Every Rule Set contains

```json
{
    "rule_version": "1.0.0",
    "status": "ACTIVE",
    "effective_date": "",
    "created_by": "",
    "description": "",
    "schema_version": "1.0"
}
```

---

# Parser Rules

```json
{
    "supported_formats": [
        "pdf",
        "docx",
        "txt"
    ],

    "ocr": {
        "enabled": true,
        "minimum_confidence": 0.90
    },

    "minimum_parser_confidence": 0.85
}
```

---

# Entity Rules

```json
{
    "minimum_confidence": 0.90,

    "alias_resolution": true,

    "ontology_resolution": true
}
```

---

# Feature Rules

```json
{
    "aggregation_strategy": "weighted_average",

    "normalization": {

        "minimum": 0,

        "maximum": 100
    }
}
```

---

# Matching Rules

```json
{
    "priority": [

        "exact",

        "alias",

        "ontology",

        "fuzzy",

        "semantic"

    ],

    "weights": {

        "exact": 1.00,

        "alias": 0.95,

        "ontology": 0.90,

        "fuzzy": 0.85,

        "semantic": 0.75

    },

    "semantic_threshold": 0.82
}
```

---

# Evidence Rules

```json
{
    "minimum_confidence": 0.85,

    "coverage_threshold": 0.80,

    "aggregation": "weighted_average"
}
```

---

# Scoring Rules

```json
{
    "weights": {

        "ats_compatibility": 20,

        "resume_quality": 20,

        "resume_jd_match": 45,

        "semantic_validation": 15

    },

    "penalties": {

        "keyword_stuffing": 5,

        "hidden_text": 10

    },

    "score_range": {

        "minimum": 0,

        "maximum": 100
    }
}
```

---

# Recommendation Rules

```json
{
    "maximum_recommendations": 20,

    "priority": {

        "critical": 6,

        "high": 4,

        "medium": 2,

        "low": 0
    },

    "publish_evidence": true,

    "publish_score_range": true
}
```

---

# Complete Example

```json
{
    "metadata": {

        "rule_version": "1.0.0",

        "status": "ACTIVE",

        "effective_date": "2026-07-12",

        "schema_version": "1.0"
    },

    "parser": {

        "minimum_parser_confidence": 0.85
    },

    "entity": {

        "minimum_confidence": 0.90
    },

    "feature": {

        "aggregation_strategy": "weighted_average"
    },

    "matching": {

        "weights": {

            "exact": 1.00,

            "alias": 0.95,

            "ontology": 0.90,

            "semantic": 0.75
        }
    },

    "evidence": {

        "minimum_confidence": 0.85
    },

    "scoring": {

        "weights": {

            "resume_jd_match": 45
        }
    },

    "recommendation": {

        "maximum_recommendations": 20
    }
}
```

---

# Rule Loading

Rule JSON is loaded during application startup.

The Rule Loader performs

- Schema Validation
- Version Validation
- Rule Validation
- Runtime Compilation

Only validated rule sets become active.

---

# Rule Versioning

Every Rule JSON records

- Rule Version
- Schema Version
- Effective Date
- Status
- Creation Timestamp

Every ATS evaluation stores the Rule Version used.

---

# Validation Rules

Validate

- Missing Metadata
- Missing Rule Categories
- Invalid Weights
- Invalid Thresholds
- Invalid Rule Version
- Duplicate Rule Keys
- Unsupported Configuration

Only validated Rule JSON may be activated.

---

# Rule Ownership

Only ATS Administrators may publish Rule JSON.

Runtime engines consume Rule JSON.

Runtime engines must never modify Rule JSON.

---

# Schema Evolution

Rules

- Existing keys must not be removed in minor versions.
- New keys must remain optional until the next major version.
- Breaking changes require a schema version increment.
- Every schema update must be documented.

---

# Dependencies

Consumes

- Rule Configuration

Produces

- Runtime Rule Objects

Consumed by

- Resume Parser
- Entity Intelligence
- Feature Engineering
- Matching Engine
- Evidence Intelligence
- ATS Scoring
- ATS Recommendation Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- 01_Parser_Rules.md
- 02_Entity_Rules.md
- 03_Feature_Rules.md
- 04_Matching_Rules.md
- 05_Evidence_Rules.md
- 06_Scoring_Rules.md
- 07_Recommendation_Rules.md

---

# End of Rule JSON Specification