# ATS Resume Intelligence Engine

# Book 00 — Project Overview

**Version:** 1.0

---

# Purpose

The ATS Resume Intelligence Engine is a deterministic resume evaluation platform that measures how well a resume is expected to perform in Applicant Tracking Systems (ATS).

The objective is to simulate ATS screening using explainable algorithms instead of black-box scoring.

The engine evaluates resumes in two modes:

1. Resume Only
2. Resume + Job Description

The scoring engine is designed to be deterministic, explainable, reproducible, and version-controlled.

---

# Objectives

The project aims to

- Build an ATS scoring engine from scratch.
- Produce consistent and reproducible ATS scores.
- Simulate real-world ATS screening behavior.
- Validate resume content using evidence-based matching.
- Prevent score manipulation through integrity checks.
- Provide explainable scoring with confidence metrics.

---

# Scope

The following modules are included.

- Resume Parsing
- Job Description Parsing
- Entity Extraction
- Feature Engineering
- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Compatibility Evaluation
- Resume Quality Evaluation
- Resume ↔ JD Matching
- Integrity Validation
- ATS Score Calculation
- Output API

---

# Out of Scope

The following modules are intentionally excluded from Version 1.

- Resume Optimization
- Resume Rewriting
- AI Resume Enhancement
- Career Guidance
- Cover Letter Generation
- Interview Preparation
- Job Recommendation Engine
- Recruiter CRM Integration

These modules will be covered in future versions.

---

# Scoring Modes

## Mode 1

Resume Only

Purpose

Evaluate the ATS readiness of a resume without a target job description.

Measures

- ATS Compatibility
- Resume Quality
- Language Quality
- Resume Completeness

---

## Mode 2

Resume + Job Description

Purpose

Evaluate how well a resume matches a specific job description.

Measures

- ATS Compatibility
- Resume Quality
- Resume ↔ JD Match
- Evidence Validation
- Integrity Validation

---

# Design Principles

The engine follows these principles.

## Deterministic

The same Resume and Job Description always produce the same score.

---

## Explainable

Every score can be traced back to measurable evidence.

---

## Evidence First

No requirement is considered matched unless supporting evidence exists.

---

## Single Source of Truth

Evidence is generated once and reused throughout the scoring pipeline.

---

## Shared Components

Resume Only and Resume + JD share common engines wherever possible.

---

## Separation of Concerns

Each engine performs one responsibility.

---

## Version Controlled

Every score is associated with version metadata.

---

# High-Level Architecture

```
Resume
Job Description

↓

Document Processing

↓

Entity Extraction

↓

Feature Engineering

↓

Knowledge Layer

↓

Evidence Intelligence

↓

ATS Compatibility

↓

Resume Quality

↓

Resume ↔ JD Matching

↓

Integrity Validation

↓

Weighted Scoring

↓

Confidence

↓

Output
```

---

# Documentation Structure

```
Book 00
Project Overview

↓

Book 01
System Architecture

↓

Book 02
Document Processing

↓

Book 03
Entity Extraction

↓

Book 04
Feature Engineering

↓

Book 05
Hybrid Knowledge Layer

↓

Book 06
Evidence Intelligence

↓

Book 07
ATS Scoring

↓

Book 08
Integrity Engine

↓

Book 09
Output API

↓

Book 10
Validation & Benchmarking
```

---

# Technology Principles

The engine uses deterministic algorithms wherever possible.

Artificial Intelligence is used only where deterministic methods are insufficient.

Examples include

- Semantic similarity
- Evidence validation
- Embedding generation

Artificial Intelligence is not used to directly calculate ATS scores.

---

# Reference Sources

The architecture and scoring methodology are inspired by publicly available information from

- Resume Worded
- Enhancv
- MyPerfectResume
- GoodSpace
- Jobscan
- HireFlow

This implementation is an independent design and does not replicate proprietary algorithms.

---

# Versioning

Every score is associated with

- Algorithm Version
- Weight Version
- Rule Version
- Knowledge Version
- Ontology Version
- Embedding Model Version
- Calibration Dataset Version

This guarantees reproducibility across engine versions.

---

# Target Audience

This documentation is intended for

- Backend Engineers
- AI Engineers
- Data Scientists
- QA Engineers
- Product Managers
- Architects

---

# Reading Order

The recommended reading order is

Book 00 → Book 01 → Book 02 → Book 03 → Book 04 → Book 05 → Book 06 → Book 07 → Book 08 → Book 09 → Book 10

Each book depends on the concepts introduced in the previous books.

---

# End of Book 00