# Skill Feature Engineering Design Document

## Book 04 — Feature Engineering | Milestone 4.2

### Purpose

This document details the architectural layout, components, and design decisions for Skill Feature Engineering (Milestone 4.2). This module maps canonical Skill entities from `CanonicalEntityCollection` into immutable generic `Feature` objects, without exposing any ATS scoring or weights.

---

### Architectural Decisions

#### 1. Grouping and Occurrence Counting
Refinement 4 dictates that exactly one `Feature` must be emitted per unique canonical skill. Duplicate skill mentions across different sections of a document are grouped by their canonical `skill_id` (or normalized raw string value if absent) and aggregated. The occurrences are structurally summed into the `occurrence_count` metadata property.

#### 2. Preservation of Raw Definitions and None IDs
In accordance with Refinement 1, we do not fabricate fake canonical IDs. If a skill entity lacks a canonical ID, `None` is explicitly preserved in the `source_entity_id` field of the feature's provenance, and raw values are mapped directly, accompanied by a validation warning log.

#### 3. Strict Structural Normalization
Only structural formatting is allowed (trimming whitespace and collapsing duplicate spaces). Lowercasing or other replacements on canonical names are forbidden to preserve exactly the terms resolved during the entity extraction phase.

---

### Component Schema

```
SkillFeatureExtractor
   ├── SkillFeatureValidator          (verifies required fields, ID prefix checks)
   ├── SkillFeatureNormalizer         (whitespace trim/collapse)
   ├── SkillFeatureBuilder            (groups duplicate counts, constructs Feature DTOs)
   └── SkillFeatureStatisticsBuilder  (telemetry logs of inputs/outputs)
```
