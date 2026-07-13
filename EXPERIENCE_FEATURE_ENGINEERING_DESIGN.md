# Experience Feature Engineering Design Document

## Book 04 — Feature Engineering | Milestone 4.3

### Purpose

This document details the architectural layout, components, and design decisions for Experience Feature Engineering (Milestone 4.3). This module maps canonical Experience entities from `CanonicalEntityCollection` into immutable generic `Feature` objects inside `FeatureCollection`.

---

### Architectural Decisions

#### 1. 1:1 Preservation without Splits
Refinement 3 states that exactly one `Feature` must be emitted per Experience entity. We never split a single job into multiple features.

#### 2. Preservation of Raw Definitions and None Fields
In accordance with Refinement 2, we do not infer missing dates, company names, or employment duration. Unknown values remain `None` in the generated feature mapping.

#### 3. No Metrics Calculation
Refinement 1 explicitly forbids calculating total experience, tenure, months, years of experience, or career progression.

#### 4. Generic Mapping Value
Refinement 2 details that `Feature.value` must hold a generic mapping of experience fields (such as `company`, `job_title`, `employment_type`, `start_date_raw`, `end_date_raw`, `responsibilities`, `technologies`, `achievements`) rather than adding experience-specific properties to the base `Feature` model.

#### 5. Strict Structural Normalization
Only whitespace trimming and duplicate space collapsing are allowed. We do not rewrite company names, job titles, or dates.

#### 6. Strongly Typed Categories
Refinement 1 migrates `Feature.category` to be fully strongly-typed using the `FeatureCategory` enum.

---

### Component Schema

```
ExperienceFeatureExtractor
   ├── ExperienceFeatureValidator          (verifies required fields, ID prefix checks)
   ├── ExperienceFeatureNormalizer         (whitespace trim/collapse)
   ├── ExperienceFeatureBuilder            (converts to Feature DTO containing generic mapping value)
   └── ExperienceFeatureStatisticsBuilder  (telemetry logs of inputs/outputs)
```
