# ATS Resume Intelligence Engine

# Recommendation JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Recommendation JSON model produced by the ATS Recommendation Engine.

Recommendation JSON is the official output of Book 08.

It contains all validated recommendations required to improve a Resume while preserving complete explainability and traceability.

Recommendation JSON is the only recommendation contract consumed by the Resume Intelligence repository.

---

# Design Principles

Recommendation JSON follows these principles.

- Deterministic
- Immutable
- Explainable
- Traceable
- Version Controlled
- Extensible

---

# Processing Flow

```
Evidence JSON

+

Score JSON

↓

Gap Analysis

↓

Recommendation Generation

↓

Recommendation Prioritization

↓

Score Impact Estimation

↓

Recommendation Validation

↓

Recommendation JSON

↓

Resume Intelligence Repository
```

---

# Recommendation JSON Structure

```json
{
    "evaluation_id": "",
    "resume_id": "",
    "job_description_id": "",

    "current_score": {},

    "summary": {},

    "recommendations": [],

    "optimization_order": [],

    "estimated_result": {},

    "versioning": {},

    "metadata": {}
}
```

---

# Evaluation Information

Contains

- Evaluation ID
- Resume ID
- Job Description ID

Example

```json
{
    "evaluation_id": "EVAL-000152",
    "resume_id": "RES-000023",
    "job_description_id": "JD-000008"
}
```

---

# Current Score

Represents the ATS score before optimization.

```json
{
    "score": 74,
    "classification": "Good"
}
```

---

# Recommendation Summary

```json
{
    "total_recommendations": 12,
    "critical": 3,
    "high": 4,
    "medium": 3,
    "low": 2
}
```

---

# Recommendation Object

Each recommendation contains

```json
{
    "recommendation_id": "",

    "category": "",

    "priority": "",

    "title": "",

    "description": "",

    "estimated_score_gain": {
        "minimum": 2,
        "maximum": 4
    },

    "impact_confidence": "",

    "related_requirement": "",

    "related_resume_section": "",

    "supporting_evidence": [],

    "reason": ""
}
```

---

# Optimization Order

Recommendations are already sorted.

```json
[
    "REC-001",
    "REC-002",
    "REC-003"
]
```

Repository 2 should process recommendations in this order.

---

# Estimated Result

Represents the predicted outcome if all recommendations are successfully implemented.

```json
{
    "current_score": 74,

    "estimated_score_range": {
        "minimum": 86,
        "maximum": 91
    },

    "confidence": "High"
}
```

The estimate is informational only.

The actual score is determined only after re-evaluation.

---

# Versioning

```json
{
    "algorithm_version": "",
    "recommendation_version": "",
    "priority_version": "",
    "validation_version": ""
}
```

---

# Metadata

```json
{
    "generated_at": "",
    "processing_time_ms": 0,
    "engine": "ATS Recommendation Engine"
}
```

---

# Complete Example

```json
{
    "evaluation_id": "EVAL-000152",

    "resume_id": "RES-000023",

    "job_description_id": "JD-000008",

    "current_score": {
        "score": 74,
        "classification": "Good"
    },

    "summary": {
        "total_recommendations": 5,
        "critical": 2,
        "high": 2,
        "medium": 1,
        "low": 0
    },

    "recommendations": [

        {
            "recommendation_id": "REC-001",

            "category": "Missing Skill",

            "priority": "Critical",

            "title": "Add Apache Spark experience",

            "description": "Demonstrate Apache Spark experience if applicable.",

            "estimated_score_gain": {
                "minimum": 3,
                "maximum": 5
            },

            "impact_confidence": "High",

            "related_requirement": "REQ-014",

            "related_resume_section": "Experience",

            "supporting_evidence": [
                "EVD-0184"
            ],

            "reason": "Required skill not supported by evidence."
        }

    ],

    "optimization_order": [
        "REC-001"
    ],

    "estimated_result": {
        "current_score": 74,
        "estimated_score_range": {
            "minimum": 86,
            "maximum": 90
        },
        "confidence": "High"
    },

    "versioning": {
        "algorithm_version": "3.2",
        "recommendation_version": "1.0",
        "priority_version": "1.0",
        "validation_version": "1.0"
    },

    "metadata": {
        "generated_at": "2026-07-12T15:00:00Z",
        "processing_time_ms": 122
    }
}
```

---

# Validation Rules

Validate

- Missing Evaluation ID
- Missing Recommendations
- Missing Priority
- Missing Evidence References
- Invalid Score Estimates
- Missing Version Information
- Broken References

Return validation failures only.

---

# Ownership

Only the ATS Recommendation Engine may create or modify Recommendation JSON.

Downstream systems consume Recommendation JSON.

They must never modify it.

---

# Schema Evolution

Rules

- Never remove existing fields in minor versions.
- New fields remain optional until the next major version.
- Breaking changes require a schema version increment.
- Every schema update must be documented.

---

# Dependencies

Consumes

- Evidence JSON
- Score JSON

Produces

- Recommendation JSON

Consumed by

- Resume Intelligence Repository
- Output API
- Dashboard
- Analytics Engine

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- 01_Gap_Analysis.md
- 02_Recommendation_Generation.md
- 03_Recommendation_Prioritization.md
- 04_Score_Impact_Estimation.md
- 05_Recommendation_Validation.md
- 07_Recommendation_API_Contract.md

---

# End of Recommendation JSON Specification