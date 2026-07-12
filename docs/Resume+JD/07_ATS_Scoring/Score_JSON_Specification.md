# ATS Resume Intelligence Engine

# Score JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Score JSON model used throughout the ATS Resume Intelligence Engine.

Score JSON is the official output of the ATS Scoring Engine.

It represents the complete scoring result for a Resume evaluated against a Job Description.

The Score JSON is immutable and becomes the single scoring contract consumed by all downstream systems.

---

# Design Principles

The Score JSON follows these principles.

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

↓

ATS Compatibility Score

↓

Resume Quality Score

↓

Resume–JD Match Score

↓

Semantic Validation Score

↓

Integrity Penalty

↓

Weighted Scoring

↓

Calibration

↓

Final ATS Score

↓

Score JSON
```

---

# Score JSON Structure

```json
{
    "evaluation_id": "",
    "resume_id": "",
    "job_description_id": "",
    "raw_score": {},
    "final_score": {},
    "component_scores": {},
    "integrity_penalty": {},
    "confidence": {},
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
    "evaluation_id": "EVAL-000142",
    "resume_id": "RES-000031",
    "job_description_id": "JD-000009"
}
```

---

# Raw Score

Represents the score before calibration.

```json
{
    "score": 84.62,
    "calibration_required": true
}
```

---

# Final Score

Represents the published ATS Score.

```json
{
    "score": 86,
    "grade": "Excellent",
    "score_band": "80-90"
}
```

---

# Component Scores

```json
{
    "ats_compatibility": {
        "score": 94.2,
        "weight": 0.20
    },

    "resume_quality": {
        "score": 90.1,
        "weight": 0.20
    },

    "resume_jd_match": {
        "score": 86.8,
        "weight": 0.45
    },

    "semantic_validation": {
        "score": 91.4,
        "weight": 0.15
    }
}
```

Every component records

- Score
- Applied Weight

---

# Integrity Penalty

```json
{
    "penalty": 3.5,
    "violations": [
        {
            "type": "Keyword Stuffing",
            "severity": "Medium"
        }
    ]
}
```

---

# Confidence

Confidence is reported separately.

It never modifies the ATS Score.

```json
{
    "overall_confidence": 98.1,
    "confidence_level": "Very High",
    "confidence_reason": "Evidence generated from validated high-confidence matches."
}
```

---

# Versioning

```json
{
    "algorithm_version": "",
    "weight_version": "",
    "calibration_version": "",
    "ontology_version": "",
    "alias_dictionary_version": "",
    "embedding_model_version": "",
    "parser_version": "",
    "pipeline_version": ""
}
```

---

# Metadata

```json
{
    "generated_at": "",
    "processing_time_ms": 0,
    "engine": "ATS Resume Intelligence Engine"
}
```

---

# Complete Example

```json
{
    "evaluation_id": "EVAL-000145",

    "resume_id": "RES-000018",

    "job_description_id": "JD-000011",

    "raw_score": {
        "score": 84.6
    },

    "final_score": {
        "score": 86,
        "grade": "Excellent",
        "score_band": "80-90"
    },

    "component_scores": {

        "ats_compatibility": {
            "score": 94.2,
            "weight": 0.20
        },

        "resume_quality": {
            "score": 91.0,
            "weight": 0.20
        },

        "resume_jd_match": {
            "score": 86.5,
            "weight": 0.45
        },

        "semantic_validation": {
            "score": 90.8,
            "weight": 0.15
        }
    },

    "integrity_penalty": {
        "penalty": 2.5
    },

    "confidence": {
        "overall_confidence": 98.3,
        "confidence_level": "Very High"
    },

    "versioning": {
        "algorithm_version": "3.2.0",
        "weight_version": "2.1",
        "calibration_version": "1.4",
        "ontology_version": "5.3",
        "embedding_model_version": "BGE-v1.5"
    },

    "metadata": {
        "generated_at": "2026-07-12T14:20:00Z",
        "processing_time_ms": 248
    }
}
```

---

# Validation Rules

Validate

- Missing Evaluation ID
- Missing Component Scores
- Invalid Weight Values
- Invalid Confidence Values
- Missing Version Information
- Invalid Final Score
- Broken Metadata

Return validation failures only.

---

# Ownership

Only the ATS Scoring Engine may create or modify Score JSON.

Downstream systems consume Score JSON.

They must never modify it.

---

# Schema Evolution

Rules

- Never remove fields in minor versions.
- New fields must remain optional until the next major version.
- Breaking changes require a schema version increment.
- Every schema update must be documented.

---

# Dependencies

Consumes

- Evidence JSON

Produces

- Score JSON

Consumed by

- Output API
- Resume Optimization Engine
- Analytics Engine
- Dashboard
- Audit Engine

---

# Related Files

- Book_07_ATS_Scoring.md
- ATS_Compatibility_Score.md
- Resume_Quality_Score.md
- Resume_JD_Match_Score.md
- Semantic_Validation_Score.md
- Integrity_Penalty.md
- Weighted_Scoring_Engine.md
- Score_Calibration.md
- Score_Versioning.md
- ATS_Final_Score.md

---

# End of Score JSON Specification