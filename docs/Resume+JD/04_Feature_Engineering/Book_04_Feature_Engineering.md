# ATS Resume Intelligence Engine

# Book 04 — Feature Engineering

**Version:** 1.0

---

# Purpose

The Feature Engineering layer transforms extracted entities into measurable business features.

Unlike Entity Extraction, which identifies and classifies information, Feature Engineering derives higher-level attributes that describe the Resume and Job Description.

These features become the primary inputs to the Hybrid Knowledge Layer and ATS Scoring Engine.

This layer performs no Resume ↔ Job Description matching and no ATS scoring.

---

# Objectives

The Feature Engineering layer is responsible for

- Deriving measurable features.
- Producing deterministic feature values.
- Preserving explainability.
- Supporting downstream matching and scoring.

---

# Scope

This book covers

- Resume Feature Engineering
- Job Description Feature Engineering
- Derived Features
- Feature Calculations
- Feature Confidence
- Feature JSON Specification

This book does not cover

- Resume ↔ JD Matching
- Semantic Search
- Evidence Generation
- ATS Scoring

---

# Processing Pipeline

```
Entity JSON

↓

Feature Extraction

↓

Derived Features

↓

Feature Validation

↓

Feature Confidence

↓

Feature JSON
```

---

# What Is A Feature?

A Feature is a measurable characteristic derived from one or more entities.

Examples

- Total Years of Experience
- Career Progression
- Skill Density
- Project Count
- Leadership Experience
- Certification Count
- Resume Completeness
- Required Skill Count
- Preferred Skill Count

---

# Feature Sources

Features are derived from

Resume

- Skills
- Experience
- Projects
- Education
- Certifications
- Summary

Job Description

- Required Skills
- Preferred Skills
- Responsibilities
- Experience Requirements
- Education Requirements
- Certifications

---

# Responsibilities

The Feature Engineering layer is responsible for

- Calculating derived values.
- Preserving calculation transparency.
- Producing deterministic Feature JSON.
- Recording feature confidence.

---

# Design Principles

## Deterministic

Identical entities always produce identical features.

---

## Explainable

Every feature must be traceable to the entities used in its calculation.

---

## No Matching

The Feature Engineering layer never compares Resume features with Job Description features.

Matching belongs to Book 05.

---

## No Scoring

The Feature Engineering layer never assigns ATS scores.

Scoring belongs to Book 07.

---

# Inputs

Consumes

- Resume Entity JSON
- Job Description Entity JSON

---

# Outputs

Produces

- Feature JSON

---

# Dependencies

Depends on

- Book 03 — Entity Extraction

Provides input to

- Book 05 — Hybrid Knowledge Layer

---

# Related Files

- Resume_Feature_Engineering.md
- JD_Feature_Engineering.md
- Derived_Features.md
- Feature_Calculation.md
- Feature_Confidence.md
- Feature_JSON_Specification.md

---

# End of Book 04