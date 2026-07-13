# Project Feature Engineering Design Document

## Book 04 — Feature Engineering | Milestone 4.5

### Purpose

This document details the architectural layout, components, and design decisions for Project Feature Engineering (Milestone 4.5). This module maps canonical Project entities from `CanonicalEntityCollection` into immutable generic `Feature` objects inside `FeatureCollection`.

---

### Architectural Decisions

#### 1. 1:1 Preservation without Splits or Merges
Refinement 3 states that exactly one `Feature` must be emitted per Project entity. We never split or merge projects.

#### 2. Preservation of Raw Definitions and None Fields
In accordance with Refinement 2, we do not infer missing project names, organizations, technologies, or URLs. Unknown values remain `None` in the generated feature mapping.

#### 3. No Metrics Calculation
Refinement 1 explicitly forbids calculating project complexity, project relevance, project duration, or technology maturity.

#### 4. Generic Mapping Value and Uniform Keys
Refinement 12 details that `Feature.value` must hold a generic mapping of project fields:
- `project_name`
- `organization`
- `role`
- `start_date_raw`
- `end_date_raw`
- `duration_raw`
- `technologies` (serializes raw technology names and canonical skill ID links)
- `responsibilities`
- `achievements`
- `repository_urls` (serializes ProjectURL structures)
- `demo_urls` (serializes ProjectURL structures)
- `location`

No project-specific fields are added to the base `Feature` model.

#### 5. Strict Structural Normalization
Only whitespace trimming and duplicate space collapsing are allowed. We do not rewrite project name text or technology values.

#### 6. Strongly Typed Categories
Refinement 5 states that we must use the strongly typed `FeatureCategory.PROJECT` category.

---

### Component Schema

```
ProjectFeatureExtractor
   ├── ProjectFeatureValidator          (verifies required fields, PROJ- ID checks)
   ├── ProjectFeatureNormalizer         (whitespace trim/collapse)
   ├── ProjectFeatureBuilder            (converts to Feature DTO containing generic mapping value)
   └── ProjectFeatureStatisticsBuilder  (telemetry logs of inputs/outputs)
```
