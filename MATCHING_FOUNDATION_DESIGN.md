# Matching Foundation Design Document

## Book 05 — Matching Engine | Milestone 5.1

### Purpose

This document details the architectural layout, components, and design decisions for the Matching Foundation (Milestone 5.1). This module acts as the infrastructure, pipeline execution, context, and registry boundary framework that concrete downstream domain matching algorithms inherit and extend.

---

### Architectural Decisions

#### 1. Immutable Matching DTOs
All match collection DTOs, results, contexts, locations, and metadata models are declared frozen to avoid modification by downstream layers (Rule 1).

#### 2. Stateless Core Engines
The execution registry, factories, pipelines, and services carry no runtime internal state or mutable singletons (Rule 2).

#### 3. Read-Only Comparison
Pipeline match processing does not mutate inputs (resume or job description canonical feature collections) (Rule 3).

#### 4. No Custom Matching Algorithms or ATS Intelligence
No similarity percentages, weighting logic, rankings, TF-IDF, embeddings, cosine calculations, or fuzzy matches are implemented at this base layer (Rules 4, 6, 7).

#### 5. Deterministic Ordering
Matches inside `MatchCollection` are sorted by `matcher_type`, `resume_feature_id`, and `job_feature_id` to ensure stable outputs (Rule 5).

---

### Component Schema

```
MatchingService
   └── MatchingPipeline
         ├── FeatureMatcherRegistry
         ├── FeatureMatcherFactory
         └── FeatureMatcher (interface)
```
