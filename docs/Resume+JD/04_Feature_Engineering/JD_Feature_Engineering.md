# ATS Resume Intelligence Engine

# JD Feature Engineering

**Version:** 1.0

---

# Purpose

The Job Description Feature Engineering module transforms Job Description Entity JSON into structured business features.

Unlike Entity Extraction, which identifies hiring requirements, this module derives measurable characteristics describing the hiring profile.

These features are later consumed by the Hybrid Knowledge Layer, Evidence Intelligence Engine, and ATS Scoring Engine.

This module performs no Resume ↔ Job Description comparison.

---

# Objectives

The module must

- Calculate deterministic features.
- Produce explainable feature values.
- Preserve calculation transparency.
- Generate Feature JSON.

---

# Inputs

Consumes

- JD Entity JSON

Produced by

- JD Entity Extraction

---

# Outputs

Produces

- JD Feature JSON

Consumed by

- Hybrid Knowledge Layer

- Evidence Intelligence

- ATS Scoring

---

# Processing Pipeline

```
JD Entity JSON

↓

Feature Selection

↓

Feature Calculation

↓

Feature Validation

↓

Feature Confidence

↓

JD Feature JSON
```

---

# Feature Categories

The Job Description Feature Engineering module derives the following feature groups.

---

## Skill Features

Examples

- Total Required Skills
- Total Preferred Skills
- Technical Skill Count
- Soft Skill Count
- Cloud Skill Count
- Programming Language Count
- Framework Count
- Tool Count
- Database Count

---

## Experience Features

Examples

- Minimum Years of Experience
- Maximum Years of Experience
- Domain Experience Required
- Industry Experience Required
- Leadership Experience Required

---

## Responsibility Features

Examples

- Total Responsibilities
- Leadership Responsibilities
- Development Responsibilities
- Architecture Responsibilities
- Management Responsibilities

---

## Technology Features

Examples

- Technology Count
- Cloud Technologies
- Databases
- Frameworks
- Programming Languages
- DevOps Tools

---

## Education Features

Examples

- Minimum Degree
- Preferred Degree
- Education Level

---

## Certification Features

Examples

- Required Certifications
- Preferred Certifications
- Cloud Certifications
- Vendor Certifications

---

## Role Features

Examples

- Seniority Level
- Employment Type
- Work Mode
- Department
- Job Category

---

## Requirement Features

Examples

- Mandatory Requirement Count
- Preferred Requirement Count
- Optional Requirement Count

---

# Feature Rules

## Rule 1

Every feature must originate from extracted entities.

Never infer missing requirements.

---

## Rule 2

Preserve explicit hiring requirements.

---

## Rule 3

Every feature must be deterministic.

---

## Rule 4

Every calculated feature must remain traceable to the originating entities.

---

## Rule 5

Feature calculations must never modify Entity JSON.

---

# Validation

Validate

- Missing required entities
- Invalid experience ranges
- Duplicate requirements
- Invalid degree values
- Invalid certifications

Return warnings only.

---

# Feature Traceability

Every feature records

- Feature Name
- Source Entities
- Calculation Method

Example

```
Minimum Experience

↓

Experience Requirement

↓

Required Skills
```

---

# Feature Confidence

Each feature includes

- Calculation Confidence

Examples

| Feature | Confidence |
|---------|-----------:|
| Required Skill Count | 100% |
| Minimum Experience | 100% |
| Leadership Requirement | 98% |
| Technology Count | 99% |

Feature Confidence measures calculation reliability only.

It never affects ATS Score.

---

# Non-Functional Requirements

The module must be

- Deterministic
- Explainable
- Stateless
- Repeatable
- Extensible

---

# Dependencies

Consumes

- JD Entity JSON

Produces

- JD Feature JSON

Consumed by

- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring

---

# Related Files

- Book_04_Feature_Engineering.md
- Resume_Feature_Engineering.md
- Derived_Features.md
- Feature_Calculation.md
- Feature_Confidence.md
- Feature_JSON_Specification.md

---

# End of JD Feature Engineering