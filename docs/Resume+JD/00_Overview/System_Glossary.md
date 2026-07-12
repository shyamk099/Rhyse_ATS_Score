# ATS Resume Intelligence Engine

# System Glossary

**Version:** 1.0

---

# Purpose

This document defines the terminology used throughout the ATS Resume Intelligence Engine.

Every book in this documentation uses these definitions.

---

# A

## Alias Matching

A matching technique that identifies equivalent names for the same skill or technology.

Example

```
JS

↓

JavaScript
```

---

## ATS

Applicant Tracking System.

Software used by recruiters to parse, filter and rank resumes before human review.

---

## ATS Compatibility

The ability of a resume to be successfully parsed and interpreted by an Applicant Tracking System.

---

# C

## Confidence

A measurement representing how reliable a detected match is.

Confidence never changes the ATS Score.

It only indicates the reliability of the supporting evidence.

---

## Calibration Dataset

A benchmark dataset used to validate and tune scoring weights.

---

# D

## Deterministic Scoring

A scoring approach where identical inputs always produce identical outputs.

---

## Document Parser

The engine responsible for converting Resume and Job Description documents into structured JSON.

---

# E

## Embedding

A numerical vector representation of text used to measure semantic similarity.

---

## Entity

A structured object extracted from a document.

Examples

- Skill
- Experience
- Project
- Education
- Certification

---

## Entity Extraction

The process of identifying structured entities from Resume and Job Description documents.

---

## Evidence

Information supporting a matched requirement.

Examples

- Experience
- Project
- Certification
- Skill
- Summary

---

## Evidence Object

A structured representation of evidence produced by the Evidence Intelligence Engine.

It is reused throughout the scoring pipeline.

---

## Evidence Intelligence Engine

The engine responsible for validating semantic relationships and producing reusable evidence.

---

# F

## Feature

A derived attribute calculated from extracted entities.

Examples

- Years of Experience
- Career Progression
- Skill Density
- Leadership Score

---

## Feature Engineering

The process of generating derived features from extracted entities.

---

## Fuzzy Matching

Matching based on approximate string similarity.

Example

```
Postgre SQL

↓

PostgreSQL
```

---

# H

## Hybrid Knowledge Layer

A matching layer that combines

- Exact Matching
- Alias Matching
- Fuzzy Matching
- Ontology Matching
- Semantic Matching

---

# I

## Integrity Engine

The engine responsible for detecting score manipulation attempts.

Examples

- Keyword Stuffing
- Hidden Text
- Fake Skills

---

# J

## Job Description

A document describing the requirements of a position.

---

# K

## Knowledge Version

The version of the knowledge resources used during scoring.

---

# M

## Match

A requirement successfully identified within the resume.

---

## Matching Engine

The engine responsible for comparing Resume entities with Job Description entities.

---

# O

## Ontology

A structured hierarchy representing relationships between technologies and concepts.

Example

```
AWS

↓

EMR

↓

Apache Spark
```

---

## Ontology Matching

Matching using relationships defined in the ontology.

---

# P

## Parser

A component that converts documents into structured information.

---

## Penalty

A score deduction produced by the Integrity Engine.

---

# R

## Requirement

A capability extracted from the Job Description.

Examples

- Skill
- Experience
- Certification
- Responsibility

---

## Resume Quality

A measure of the overall quality of resume content.

---

# S

## Semantic Matching

Matching based on contextual meaning rather than exact wording.

---

## Semantic Similarity

A numerical measurement representing how closely two pieces of text are related.

---

## Shared Component

A component reused by both Resume Only and Resume + JD scoring modes.

---

## Structured Resume

The JSON representation of a parsed resume.

---

## Structured Job Description

The JSON representation of a parsed Job Description.

---

# V

## Version Metadata

Metadata identifying the exact configuration used to calculate a score.

Includes

- Algorithm Version
- Weight Version
- Rule Version
- Knowledge Version
- Ontology Version
- Embedding Model Version
- Calibration Dataset Version

---

# W

## Weighted Score

The calculated ATS score before Integrity Penalties are applied.

---

# End of Glossary