# ATS Resume Intelligence Engine

# Book 09 — ATS Rule Engine

**Version:** 1.0

---

# Purpose

The ATS Rule Engine provides the centralized business rules and configuration used by every intelligence component in the ATS Resume Intelligence Engine.

The Rule Engine separates business policy from application logic.

It allows parser behavior, entity extraction, feature engineering, matching, evidence generation, scoring, and recommendations to be configured without modifying source code.

The Rule Engine never performs ATS processing.

It only supplies rules to the processing engines.

---

# Objectives

The ATS Rule Engine must

- Centralize business rules.
- Eliminate hardcoded configuration.
- Support rule versioning.
- Support rule validation.
- Support configurable ATS behavior.
- Preserve deterministic execution.

---

# Scope

This book covers

- Parser Rules
- Entity Rules
- Feature Rules
- Matching Rules
- Evidence Rules
- Scoring Rules
- Recommendation Rules
- Rule Configuration
- Rule Versioning

This book does not cover

- Resume Parsing
- Resume Matching
- ATS Scoring
- Recommendation Generation

These engines consume rules.

They never define rules.

---

# Inputs

Consumes

- Rule Configuration Files

Produced by

- Business Configuration
- ATS Administrators

---

# Outputs

Produces

Runtime Rule Objects

Consumed by

- Resume Parser
- Entity Intelligence
- Feature Engineering
- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring
- ATS Recommendation Engine

---

# Rule Philosophy

The Rule Engine answers one question.

> "How should the ATS behave?"

The Rule Engine never answers

> "How should a Resume be processed?"

Processing belongs to the intelligence engines.

Configuration belongs to the Rule Engine.

---

# Architecture

```
Configuration Files

↓

Rule Loader

↓

Rule Validation

↓

Rule Objects

↓

Parser

↓

Entity

↓

Feature

↓

Matching

↓

Evidence

↓

Scoring

↓

Recommendation
```

---

# Rule Categories

The Rule Engine manages

## Parser Rules

Controls

- Supported file types
- OCR thresholds
- Section detection
- Encoding
- Header detection

---

## Entity Rules

Controls

- Entity aliases
- Entity normalization
- Entity confidence thresholds
- Validation rules

---

## Feature Rules

Controls

- Feature extraction thresholds
- Experience calculations
- Education rules
- Skill extraction
- Certification extraction

---

## Matching Rules

Controls

- Exact Match weight
- Alias Match weight
- Ontology Match weight
- Fuzzy Match threshold
- Semantic Match threshold

---

## Evidence Rules

Controls

- Evidence confidence
- Coverage thresholds
- Validation rules
- Aggregation rules

---

## Scoring Rules

Controls

- Component weights
- Penalty values
- Calibration rules
- Score boundaries
- Grade definitions

---

## Recommendation Rules

Controls

- Priority thresholds
- Recommendation categories
- Estimated score gain limits
- Recommendation validation rules

---

# Rule Lifecycle

```
Rule File

↓

Load

↓

Validate

↓

Compile

↓

Cache

↓

Runtime Rule Object

↓

Consumed by ATS Engines
```

---

# Rule Loading

Rules are loaded during application startup.

Rule updates require

- Rule Validation
- Version Increment
- Reload

The loading strategy is configurable.

---

# Rule Versioning

Every rule set contains

- Rule Version
- Rule Category
- Effective Date
- Status
- Author
- Description

Every ATS evaluation records the rule version used.

---

# Rule Hierarchy

Rules are evaluated in the following order

1. Global Rules
2. Engine Rules
3. Category Rules
4. Runtime Overrides

Lower-level rules may override higher-level rules only when explicitly allowed.

---

# Rule Validation

Every rule file must be validated before activation.

Validate

- Schema
- Required Fields
- Duplicate Keys
- Invalid Values
- Invalid Thresholds
- Invalid Weights
- Circular References

Only validated rules may become active.

---

# Design Principles

## Configurable

Business behavior must be configurable.

---

## Deterministic

The same rule set must always produce the same behavior.

---

## Versioned

Every rule set is version controlled.

---

## Traceable

Every ATS evaluation records the rule version.

---

## Immutable

Activated rule versions never change.

---

## Independent

Each engine consumes only the rules relevant to it.

---

# Rule Rules

## Rule 1

Business rules must never be hardcoded.

---

## Rule 2

Every rule belongs to exactly one category.

---

## Rule 3

Rule changes require version increments.

---

## Rule 4

Invalid rules must never be activated.

---

## Rule 5

Rule execution must be deterministic.

---

## Rule 6

Rules are read-only during ATS execution.

---

## Rule 7

Runtime engines never modify rules.

---

# Example

```
Matching Rule

↓

Semantic Weight

↓

0.75

↓

Rule Engine

↓

Matching Engine
```

---

Another Example

```
Scoring Rule

↓

Resume–JD Weight

↓

45%

↓

Rule Engine

↓

Scoring Engine
```

---

# Non-Functional Requirements

The Rule Engine must be

- Deterministic
- Stateless
- Immutable
- Versioned
- Auditable
- Extensible

---

# Dependencies

Consumes

- Rule Configuration Files

Produces

- Runtime Rule Objects

Consumed by

- Parser
- Entity Engine
- Feature Engine
- Matching Engine
- Evidence Engine
- Scoring Engine
- Recommendation Engine

---

# Related Files

- 01_Parser_Rules.md
- 02_Entity_Rules.md
- 03_Feature_Rules.md
- 04_Matching_Rules.md
- 05_Evidence_Rules.md
- 06_Scoring_Rules.md
- 07_Recommendation_Rules.md
- 08_Rule_JSON_Specification.md

---

# End of Book 09