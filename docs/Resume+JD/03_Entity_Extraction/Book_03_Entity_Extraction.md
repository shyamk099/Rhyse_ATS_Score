# ATS Resume Intelligence Engine

# Book 03 — Entity Extraction

**Version:** 1.0

---

# Purpose

The Entity Extraction layer transforms structured Resume and Job Description documents into standardized business entities.

Unlike the parser, which preserves document structure, Entity Extraction identifies meaningful business objects that will later be used for matching, feature engineering, and scoring.

This layer performs no scoring.

---

# Objectives

The Entity Extraction layer is responsible for

- Identifying business entities.
- Classifying extracted entities.
- Preserving entity provenance.
- Producing deterministic entities.
- Reporting extraction confidence.

---

# Scope

This book covers

- Resume Entity Extraction
- Job Description Entity Extraction
- Entity Classification
- Entity Confidence
- Entity Relationships
- Entity Normalization

This book does not cover

- Feature Engineering
- ATS Scoring
- Resume Matching
- Semantic Search

---

# Processing Pipeline

```
Resume JSON

+

JD JSON

↓

Entity Detection

↓

Entity Classification

↓

Entity Normalization

↓

Relationship Mapping

↓

Confidence Assignment

↓

Entity JSON
```

---

# What Is An Entity?

An Entity is a meaningful business object extracted from a document.

Examples

- Skill
- Company
- Job Title
- Technology
- Programming Language
- Certification
- Degree
- Institution
- Project
- Responsibility
- Tool
- Framework
- Cloud Platform
- Database
- Location
- Date

---

# Entity Sources

Entities may originate from

Resume

- Skills
- Experience
- Projects
- Summary
- Certifications
- Education

Job Description

- Requirements
- Responsibilities
- Technical Stack
- Preferred Skills
- Qualifications

---

# Entity Lifecycle

```
Document

↓

Parser

↓

Structured JSON

↓

Entity Detection

↓

Normalization

↓

Relationship Mapping

↓

Confidence

↓

Entity JSON
```

---

# Responsibilities

The Entity Extraction layer is responsible for

- Detecting entities.
- Classifying entities.
- Normalizing entity values.
- Preserving source information.
- Recording confidence.
- Producing Entity JSON.

---

# Design Principles

The Entity Extraction layer follows these principles.

## Deterministic

Identical inputs always produce identical entities.

---

## Preserve Source

Original values are never discarded.

---

## No Inference

Only explicitly identified entities are extracted.

Inference belongs to later intelligence layers.

---

## Single Responsibility

Entity Extraction only extracts entities.

It does not calculate

- ATS Scores
- Feature Values
- Semantic Similarity

---

# Inputs

Consumes

- Resume JSON
- Job Description JSON

---

# Outputs

Produces

- Entity JSON

---

# Dependencies

Depends on

- Book 02 — Document Processing

Provides input to

- Book 04 — Feature Engineering

---

# Related Files

- Resume_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Confidence.md
- Entity_Relationships.md
- Entity_JSON_Specification.md

---

# End of Book 03