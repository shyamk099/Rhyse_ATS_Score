# Certification Feature Engineering Design Document

## Book 04 — Feature Engineering | Milestone 4.5

### Purpose

This document details the architectural layout, components, and design decisions for Certification Feature Engineering (Milestone 4.5). This module maps canonical Certification entities from `CanonicalEntityCollection` into immutable generic `Feature` objects inside `FeatureCollection`.

---

### Architectural Decisions

#### 1. 1:1 Preservation without Splits or Merges
Refinement 3 states that exactly one `Feature` must be emitted per Certification entity.

#### 2. Preservation of Raw Definitions and None Fields
In accordance with Refinement 2, we do not infer issuing organizations, expiration dates, or credential IDs. Unknown values remain `None` in the generated feature mapping.

#### 3. No Metrics Calculation
Refinement 1 explicitly forbids calculating certification validity, certification expiration, ranking, or weights.

#### 4. Generic Mapping Value and Uniform Keys
Refinement 12 details that `Feature.value` must hold a generic mapping of certification fields:
- `certification_name`
- `issuing_organization`
- `credential_id` (maps from `credential_id_raw`)
- `credential_url` (serializes CertificationURL)
- `issue_date_raw`
- `expiration_date_raw`
- `validity_status_raw`
- `associated_skill_ids`
- `associated_skills` (maps from `associated_skills_raw`)
- `description` (maps from `description_raw`)

No certification-specific fields are added to the base `Feature` model.

#### 5. Strict Structural Normalization
Only whitespace trimming and duplicate space collapsing are allowed. We do not rewrite certification names, issuers, or credential IDs.

#### 6. Strongly Typed Categories
Refinement 5 states that we must use the strongly typed `FeatureCategory.CERTIFICATION` category.

---

### Component Schema

```
CertificationFeatureExtractor
   ├── CertificationFeatureValidator          (verifies required fields, CERT- ID checks)
   ├── CertificationFeatureNormalizer         (whitespace trim/collapse)
   ├── CertificationFeatureBuilder            (converts to Feature DTO containing generic mapping value)
   └── CertificationFeatureStatisticsBuilder  (telemetry logs of inputs/outputs)
```
