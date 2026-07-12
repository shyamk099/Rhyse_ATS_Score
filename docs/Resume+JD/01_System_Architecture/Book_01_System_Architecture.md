# ATS Resume Intelligence Engine

# Book 01 — System Architecture

**Version:** 1.0

---

# Purpose

This document defines the overall architecture of the ATS Resume Intelligence Engine.

It explains how every component in the platform interacts to produce a deterministic, explainable, and evidence-based ATS score.

All implementation must conform to this architecture.

---

# Objectives

The architecture is designed to achieve the following objectives.

- Deterministic ATS Scoring
- Modular System Design
- Explainable Results
- Evidence-Based Matching
- Reusable Components
- Version Controlled Scoring
- Scalable API Architecture

---

# Architectural Principles

The system follows the principles defined in **Book 00 – Architecture Decision Records**.

These principles are mandatory.

## Deterministic

Identical inputs always produce identical outputs.

---

## Explainable

Every score must be explainable.

---

## Evidence First

Every matched requirement must have supporting evidence.

---

## Single Source of Truth

Evidence is generated once and reused throughout the platform.

---

## Shared Components

Common engines are reused across Resume Only and Resume + JD modes.

---

## Separation of Concerns

Each engine owns one responsibility.

---

## Version Controlled

Every scoring request is reproducible.

---

# System Layers

The ATS Resume Intelligence Engine is divided into five logical layers.

```
Presentation Layer

↓

Processing Layer

↓

Intelligence Layer

↓

Scoring Layer

↓

Output Layer
```

Each layer has a clearly defined responsibility.

---

# Layer 1 — Presentation Layer

Responsible for receiving input from external systems.

Components

- Resume Upload
- Job Description Upload
- REST API
- Authentication
- Request Validation

Input

- Resume
- Job Description

Output

- Validated Request

---

# Layer 2 — Processing Layer

Responsible for converting documents into structured information.

Components

- Document Parser
- Entity Extraction
- Feature Engineering

Output

- Structured Resume
- Structured Job Description
- Feature Objects

---

# Layer 3 — Intelligence Layer

Responsible for understanding relationships between the Resume and Job Description.

Components

- Hybrid Knowledge Layer
- Evidence Intelligence Engine

Output

- Evidence Objects
- Match Relationships
- Requirement Confidence

---

# Layer 4 — Scoring Layer

Responsible for ATS evaluation.

Components

- ATS Compatibility Engine
- Resume Quality Engine
- Resume ↔ JD Matching Engine
- Integrity Engine
- Weighted Score Engine

Output

- ATS Score

---

# Layer 5 — Output Layer

Responsible for generating the final API response.

Components

- Confidence Aggregator
- Output Engine

Output

- ATS Score
- Section Scores
- Evidence
- Confidence
- JSON Response

---

# High-Level Architecture

```
Presentation Layer

↓

Processing Layer

↓

Intelligence Layer

↓

Scoring Layer

↓

Output Layer
```

---

# Engine Overview

| Engine | Responsibility |
|---------|----------------|
| Document Parser | Parse Resume and JD |
| Entity Extraction | Extract structured entities |
| Feature Engineering | Generate derived features |
| Hybrid Knowledge Layer | Match using Exact, Alias, Fuzzy, Ontology and Semantic methods |
| Evidence Intelligence | Validate evidence and generate Evidence Objects |
| ATS Compatibility | Evaluate ATS readiness |
| Resume Quality | Evaluate resume quality |
| Resume ↔ JD Matching | Evaluate job alignment |
| Integrity Engine | Detect score manipulation |
| Weighted Score Engine | Calculate final ATS score |
| Confidence Aggregator | Aggregate confidence metrics |
| Output Engine | Produce API response |

---

# Shared Components

The following engines are shared by every scoring mode.

- Document Parser
- Entity Extraction
- Feature Engineering
- Hybrid Knowledge Layer
- Evidence Intelligence Engine
- ATS Compatibility Engine
- Resume Quality Engine
- Integrity Engine
- Confidence Aggregator
- Output Engine

Only the Resume ↔ JD Matching Engine is exclusive to Resume + JD mode.

---

# Data Flow

```
Input

↓

Parser

↓

Entity Extraction

↓

Feature Engineering

↓

Knowledge Layer

↓

Evidence Intelligence

↓

Scoring

↓

Confidence

↓

Output
```

---

# Architectural Constraints

The following constraints are mandatory.

- No engine performs multiple responsibilities.
- Semantic validation executes only once.
- Resume Quality is shared across scoring modes.
- Integrity penalties are capped.
- Final scores are clamped between 0 and 100.
- Confidence never changes the ATS score.
- Every matched requirement must have evidence.

---

# Dependencies

This document depends on

- Product Vision
- Project Overview
- System Glossary
- Architecture Decision Records

The remaining books depend on this document.

---

# Related Books

Book 02 — Document Processing

Book 03 — Entity Extraction

Book 04 — Feature Engineering

Book 05 — Hybrid Knowledge Layer

Book 06 — Evidence Intelligence

Book 07 — ATS Scoring

Book 08 — Integrity Engine

Book 09 — Output API

Book 10 — Validation

---

# End of Book 01