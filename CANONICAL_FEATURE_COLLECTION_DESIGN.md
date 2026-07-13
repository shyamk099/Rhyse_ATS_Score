# Canonical Feature Collection Design Document

## Book 04 — Feature Engineering | Milestone 4.6

### Purpose

This document details the architectural layout, components, and design decisions for Canonical Feature Collection (Milestone 4.6). This module acts as the consolidated validation, deduplication, and aggregation boundary contract separating Book 04 from downstream Matching (Book 05) and Scoring (Book 06) modules.

---

### Architectural Decisions

#### 1. Read-Only Feature Validation
Refinement 1 specifies validators are read-only. We compile error and warning details without mutating the raw feature definitions.

#### 2. Duplicate Resolution Policies
Refinement 2 defines that duplicate resolution strictly follows standard configuration policies:
* `KEEP_FIRST`: Keep the first occurrence.
* `KEEP_LAST`: Keep the last occurrence.
* `KEEP_HIGHEST_CONFIDENCE`: Keep the occurrence with the highest confidence score.
* `KEEP_ALL`: Keep all occurrences.

No custom merge logic is performed.

#### 3. Cross-Validation Verification
Refinement 3 states that cross-validation verifies relational references (e.g. unique ID checks across the collection, category-provenance mismatches) without correcting.

#### 4. Statistics Compile counts Only
Refinement 4 specifies statistics contain structural metrics only. Category counts, warning counts, duplicate counts, and `total_feature_count` are compiled. No quality scores or importance weights.

#### 5. Deterministic Ordering
Refinement 5 dictates sorting features inside each Category collection deterministically by `feature_id` to ensure stable ordering across multiple runs.

---

### Component Schema

```
CanonicalFeatureCollectionService
   └── CanonicalFeatureCollectionPipeline
         ├── FeatureValidator
         ├── DuplicateFeatureResolver
         ├── CrossFeatureValidator
         ├── FeatureStatisticsBuilder
         ├── ValidationSummaryBuilder
         └── CanonicalFeatureCollectionBuilder
```
