# Skill Matching Design Document

## Book 05 — Matching Engine | Milestone 5.2

### Purpose

This document details the architectural layout, components, and design decisions for Skill Matching (Milestone 5.2). This module compares Resume Skill Features against Job Description Skill Features using deterministic identifier-based exact matching.

---

### Architectural Decisions

#### 1. Exact Matching Only
Rule 1 specifies that matches occur ONLY when canonical identifiers are identical. Raw matching (by normalized name strings) is only allowed as a fallback if comparison_mode is configured to "ALL".

#### 2. No Similarity Metric or Weights
Rule 2 & 3 forbid calculating cosine similarity, TF-IDF, embeddings, vector search, edit distances, percentage rates, or relevance weights. We determine only whether a structural match exists.

#### 3. Read-Only Compilation
Rule 4 guarantees resume and job description feature collections are read-only and unmutated.

#### 4. One Match Per Pair
Rule 5 ensures one resume feature + one job feature matches exactly to one MatchResult (no group merges).

#### 5. Deterministic Ordering
Rule 7 ensures output lists are sorted by `matcher_type`, `resume_feature_id`, and `job_feature_id`.

---

### Component Schema

```
SkillMatcher
   ├── SkillMatchCandidateBuilder
   ├── SkillMatchValidator
   ├── SkillMatchNormalizer
   └── SkillMatchBuilder
```
