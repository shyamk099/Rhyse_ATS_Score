# ATS Resume Intelligence Engine

# Recommendation Rules

**Version:** 1.0

---

# Purpose

The Recommendation Rules Engine defines the configurable business rules used by the ATS Recommendation Engine.

Recommendation Rules determine how recommendations are classified, prioritized, filtered, grouped, and published.

Recommendation Rules never generate recommendations.

They only define the recommendation policy.

---

# Objectives

The Recommendation Rules Engine must

- Configure recommendation priorities.
- Configure recommendation categories.
- Configure recommendation filtering.
- Configure impact thresholds.
- Configure publication rules.
- Preserve deterministic recommendation behavior.

---

# Scope

This module covers

- Category Rules
- Priority Rules
- Impact Rules
- Filtering Rules
- Grouping Rules
- Validation Rules
- Publication Rules

This module does not cover

- Gap Analysis
- Recommendation Generation
- Resume Rewriting
- ATS Scoring

---

# Inputs

Consumes

- Recommendation Rule Configuration

Produced by

- ATS Administrator
- Business Configuration

---

# Outputs

Produces

- Runtime Recommendation Rules

Consumed by

- ATS Recommendation Engine

---

# Rule Philosophy

Recommendation Rules answer one question.

> "How should recommendations be prioritized and presented?"

The ATS Recommendation Engine generates recommendations.

The Rule Engine defines how those recommendations are evaluated and published.

---

# Processing Pipeline

```
Recommendation Rule Configuration

↓

Rule Loader

↓

Rule Validation

↓

Runtime Recommendation Rules

↓

ATS Recommendation Engine
```

---

# Rule Categories

## Category Rules

Defines supported recommendation categories.

Examples

- Missing Skill
- Missing Experience
- Missing Project
- Missing Certification
- Resume Quality
- ATS Compatibility
- Keyword Coverage
- Leadership
- Education

Individual categories may be enabled or disabled.

---

## Priority Rules

Defines

- Critical Threshold
- High Threshold
- Medium Threshold
- Low Threshold

Priority thresholds are configurable.

Example

```
Estimated Score Gain

≥ 6

↓

Priority

Critical
```

---

## Impact Rules

Defines

- Minimum Estimated Gain
- Maximum Estimated Gain
- Confidence Threshold
- Business Importance Threshold

Only recommendations meeting configured criteria are published.

---

## Filtering Rules

Defines

- Maximum Recommendations
- Duplicate Removal
- Low Value Filtering
- Hidden Categories

Example

```
Maximum Recommendations

20
```

Filtering behavior is configurable.

---

## Grouping Rules

Defines whether recommendations should be grouped.

Examples

```
Missing Skills

↓

One Group
```

```
Resume Formatting

↓

One Group
```

Grouping strategy is configurable.

---

## Publication Rules

Defines

- Publish Warnings
- Publish Low Priority Items
- Publish Estimated Score Range
- Publish Evidence References

Publication behavior is configurable.

---

## Validation Rules

Defines

- Duplicate Recommendations
- Missing Evidence
- Missing Requirement References
- Invalid Priorities
- Invalid Categories

Only valid recommendations are published.

---

# Rule Lifecycle

```
Configuration

↓

Validation

↓

Activation

↓

Recommendation Engine
```

---

# Rule Validation

Validate

- Missing Rules
- Duplicate Rules
- Invalid Priority Thresholds
- Invalid Score Gain Limits
- Invalid Categories
- Invalid Filtering Rules

Only validated rule sets become active.

---

# Design Principles

## Configurable

Recommendation policy must never be hardcoded.

---

## Deterministic

The same Recommendation Objects with the same rules must always produce identical output.

---

## Versioned

Every Recommendation Rule set has a version.

---

## Immutable

Rules cannot change during execution.

---

## Traceable

Every Recommendation JSON records the Recommendation Rule Version.

---

# Example Configuration

```yaml
recommendation:

  categories:

    missing_skill:
      enabled: true

    ats_formatting:
      enabled: true

    education:
      enabled: false

  priority:

    critical:
      minimum_gain: 6

    high:
      minimum_gain: 4

    medium:
      minimum_gain: 2

    low:
      minimum_gain: 0

  filtering:

    maximum_recommendations: 20

    remove_duplicates: true

  grouping:

    enabled: true

  publication:

    publish_score_range: true

    publish_evidence: true
```

---

# Rule Rules

## Rule 1

Recommendation priorities must be configurable.

---

## Rule 2

Filtering behavior must be configurable.

---

## Rule 3

Rules are read-only during execution.

---

## Rule 4

Invalid Recommendation Rules must never be activated.

---

## Rule 5

Every Recommendation JSON records the Recommendation Rule Version.

---

## Rule 6

Runtime engines cannot modify Recommendation Rules.

---

# Dependencies

Consumes

- Recommendation Rule Configuration

Produces

- Runtime Recommendation Rules

Consumed by

- ATS Recommendation Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- Parser_Rules.md
- Entity_Rules.md
- Feature_Rules.md
- Matching_Rules.md
- Evidence_Rules.md
- Scoring_Rules.md
- Rule_JSON_Specification.md

---

# End of Recommendation Rules