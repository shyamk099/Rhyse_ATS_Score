# Experience Matching Design Document

## Book 05 — Matching Engine | Milestone 5.3

### Purpose

This document details the architectural layout, components, and design decisions for Experience Matching (Milestone 5.3). This module compares Resume Experience Features with Job Description Experience Features based on deterministic structural fields and canonical IDs.

---

### Architectural Decisions

#### 1. Precedence Logic
If both Resume and Job experience features contain the same canonical `experience_id`, the match is determined by the canonical ID comparison first. Otherwise, it compares structural company name and job title fields.

#### 2. Comparison on Normalized Copies
Candidate features are structurally normalized (whitespace collapse, casing checks) in duplicated copies before comparison evaluations, ensuring that original collection structures remain unmutated (Rules 5, 10).

#### 3. No Durations Math or career calculations
Rule 2 forbids calculating months of experience, career progression, recency, promotions, or seniority levels.

#### 4. Compound Entity Integrity
Rule 11 ensures that compound Experience features are treated as single cohesive entities. We do not split experience features into multiple MatchResults or merge multiple experiences into one result.

#### 5. Deterministic Ordering
Rule 8 ensures output lists are sorted by `matcher_type`, `resume_feature_id`, and `job_feature_id`.

---

### Component Schema

```
ExperienceMatcher
   ├── ExperienceMatchCandidateBuilder
   ├── ExperienceMatchValidator
   ├── ExperienceMatchNormalizer
   └── ExperienceMatchBuilder
```
