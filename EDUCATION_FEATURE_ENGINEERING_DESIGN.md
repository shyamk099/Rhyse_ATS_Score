# Education Feature Engineering Design Document

## Book 04 — Feature Engineering | Milestone 4.4

### Purpose

This document details the architectural layout, components, and design decisions for Education Feature Engineering (Milestone 4.4). This module maps canonical Education entities from `CanonicalEntityCollection` into immutable generic `Feature` objects inside `FeatureCollection`.

---

### Architectural Decisions

#### 1. 1:1 Preservation without Splits
Refinement 3 states that exactly one `Feature` must be emitted per Education entity. We never split an education record into multiple features.

#### 2. Preservation of Raw Definitions and None Fields
In accordance with Refinement 2, we do not infer missing graduation dates, institution names, honors, or GPA values. Unknown values remain `None` in the generated feature mapping.

#### 3. No Metrics Calculation
Refinement 1 explicitly forbids calculating study duration, study years, GPA evaluation, academic ranking, or degree equivalency.

#### 4. Generic Mapping Value and Uniform Keys
Refinement 11 and user recommendations dictate that `Feature.value` must hold a generic mapping of education fields with strict uniform key naming:
- `institution`
- `degree`
- `major`
- `specialization`
- `start_date_raw`
- `end_date_raw`
- `graduation_date_raw`
- `gpa`
- `grade`
- `honors`
- `certifications`
- `location`

We avoid variants like `university`, `school`, `cgpa`, or `degree_name`. No education-specific properties are added to the base `Feature` model.

#### 5. Strict Structural Normalization
Only whitespace trimming and duplicate space collapsing are allowed (Refinement 6).

#### 6. Strongly Typed Categories
Refinement 5 states that we must use the `FeatureCategory.EDUCATION` enum value.

---

### Component Schema

```
EducationFeatureExtractor
   ├── EducationFeatureValidator          (verifies required fields, ID prefix checks)
   ├── EducationFeatureNormalizer         (whitespace trim/collapse)
   ├── EducationFeatureBuilder            (converts to Feature DTO containing generic mapping value)
   └── EducationFeatureStatisticsBuilder  (telemetry logs of inputs/outputs)
```
