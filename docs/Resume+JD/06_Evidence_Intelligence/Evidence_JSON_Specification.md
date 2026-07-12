# ATS Resume Intelligence Engine

# Evidence JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Evidence JSON model used throughout the ATS Resume Intelligence Engine.

Evidence JSON is the official output of the Evidence Intelligence Layer.

It represents all validated, aggregated, and explainable evidence generated from the Resume and Job Description comparison.

Evidence JSON is the only evidence contract consumed by downstream engines.

---

# Design Principles

Evidence JSON follows these principles.

- Deterministic
- Immutable
- Explainable
- Traceable
- Version Controlled
- Extensible

---

# Processing Flow

```
Match JSON

↓

Evidence Generation

↓

Requirement Evidence

↓

Section Evidence

↓

Evidence Validation

↓

Evidence Confidence

↓

Evidence Aggregation

↓

Explainability

↓

Evidence JSON

↓

ATS Scoring
```

---

# Evidence JSON Structure

Every Resume evaluation produces one Evidence JSON document.

```json
{
  "evaluation_id": "",
  "resume_id": "",
  "job_description_id": "",
  "requirements": [],
  "resume_sections": [],
  "evidence": [],
  "coverage": {},
  "confidence": {},
  "summary": {},
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
  "evaluation_id": "EVAL-000125",
  "resume_id": "RES-000018",
  "job_description_id": "JD-000011"
}
```

---

# Requirements

Each Job Description requirement contains

```json
{
  "requirement_id": "",
  "requirement_name": "",
  "requirement_type": "",
  "status": "",
  "coverage_percentage": 0,
  "evidence_ids": [],
  "confidence": 0.0
}
```

---

# Resume Sections

Each Resume section contains

```json
{
  "section_id": "",
  "section_name": "",
  "status": "",
  "evidence_count": 0,
  "requirement_count": 0,
  "confidence": 0.0
}
```

---

# Evidence

Each Evidence Object contains

```json
{
  "evidence_id": "",
  "match_id": "",
  "resume_feature_id": "",
  "jd_feature_id": "",
  "evidence_type": "",
  "matching_strategy": "",
  "description": "",
  "confidence": {},
  "metadata": {}
}
```

---

# Coverage

Coverage summarizes overall Resume ↔ JD alignment.

```json
{
  "requirement_coverage": 0.0,
  "skill_coverage": 0.0,
  "experience_coverage": 0.0,
  "project_coverage": 0.0,
  "certification_coverage": 0.0,
  "education_coverage": 0.0
}
```

Coverage is descriptive.

Coverage is not the ATS Score.

---

# Confidence

Evidence JSON contains overall evidence confidence.

```json
{
  "overall_confidence": 0.0,
  "confidence_level": "",
  "confidence_reason": ""
}
```

Confidence explains reliability.

Confidence never changes ATS Score.

---

# Summary

Summary contains

```json
{
  "total_requirements": 0,
  "requirements_matched": 0,
  "requirements_missing": 0,
  "total_evidence": 0,
  "resume_sections_used": 0
}
```

---

# Metadata

Metadata records

```json
{
  "algorithm_version": "",
  "pipeline_version": "",
  "evidence_version": "",
  "match_schema_version": "",
  "generated_at": ""
}
```

---

# Complete Example

```json
{
  "evaluation_id": "EVAL-000145",
  "resume_id": "RES-000041",
  "job_description_id": "JD-000012",

  "requirements": [
    {
      "requirement_id": "REQ-001",
      "requirement_name": "Python",
      "status": "Fully Satisfied",
      "coverage_percentage": 100,
      "confidence": 99.2
    }
  ],

  "resume_sections": [
    {
      "section_name": "Experience",
      "status": "Excellent",
      "evidence_count": 12,
      "confidence": 98.7
    }
  ],

  "coverage": {
    "requirement_coverage": 87.5,
    "skill_coverage": 90.0,
    "experience_coverage": 84.0
  },

  "confidence": {
    "overall_confidence": 98.1,
    "confidence_level": "Very High",
    "confidence_reason": "Evidence generated from validated high-confidence matches."
  },

  "summary": {
    "total_requirements": 24,
    "requirements_matched": 21,
    "requirements_missing": 3,
    "total_evidence": 67,
    "resume_sections_used": 5
  },

  "metadata": {
    "algorithm_version": "1.0",
    "pipeline_version": "1.0",
    "evidence_version": "1.0",
    "match_schema_version": "1.0"
  }
}
```

---

# Validation Rules

Validate

- Duplicate Evaluation IDs
- Missing Requirement IDs
- Missing Evidence IDs
- Invalid Coverage Values
- Invalid Confidence Values
- Broken References
- Missing Metadata

Return validation failures only.

---

# Ownership

Only the Evidence Intelligence Layer may create or modify Evidence JSON.

Downstream modules consume Evidence JSON.

They must never modify it.

---

# Schema Evolution

Rules

- Never remove existing fields in minor versions.
- New fields must remain optional until the next major version.
- Breaking changes require a schema version increment.
- Schema updates must be documented before implementation.

---

# Dependencies

Consumes

- Match JSON

Produces

- Evidence JSON

Consumed by

- ATS Scoring Engine
- Output API
- Resume Optimization Engine
- Analytics Engine

---

# Related Files

- Book_06_Evidence_Intelligence.md
- 01_Evidence_Generation.md
- 02_Requirement_Evidence.md
- 03_Section_Evidence.md
- 04_Evidence_Validation.md
- 05_Evidence_Confidence.md
- 06_Evidence_Aggregation.md
- 07_Explainability_Model.md

---

# End of Evidence JSON Specification