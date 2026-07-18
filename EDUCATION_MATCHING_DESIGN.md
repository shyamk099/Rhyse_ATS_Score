# Education Matching Design Document

## Book 05 — Matching Engine | Milestone 5.4

### Purpose

This document details the architectural layout, components, and design decisions for Education Matching (Milestone 5.4). This module compares Resume Education Features against Job Description Education Features using deterministic structural precedence.

---

### Architectural Decisions

#### 1. Progressive Precedence Ordering
Matches are evaluated from most-specific to least-specific properties:
1. Canonical Education ID
2. Institution + Degree + Major + Specialization
3. Institution + Degree + Major
4. Institution + Degree

If canonical IDs match, lower precedence rules are immediately bypassed.

#### 2. Reusable Matching Utilities
Centralized string and dictionary matching helpers are introduced under `matching/common/comparison.py` to prevent code duplication across Education, Project, and Certification matchers.

#### 3. Empty Candidates Filter
Validation rules bypass pairing and comparisons where both resume and job features have all matching properties (institution, degree, major, specialization) empty or None.

#### 4. Immutability & Statelessness
Candidate Feature structures are normalized inside copies, ensuring collections remain completely read-only. Every processor is stateless and thread-safe.

---

### Component Schema

```
EducationMatcher
   ├── EducationMatchCandidateBuilder (filters empty records)
   ├── EducationMatchValidator
   ├── EducationMatchNormalizer (normalizes copies)
   ├── matching.common.comparison (reusable compare helpers)
   └── EducationMatchBuilder
```
