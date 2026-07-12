# ATS Resume Intelligence Engine

# Feature Calculation

**Version:** 1.0

---

# Purpose

This document defines the calculation methodology for every feature used by the ATS Resume Intelligence Engine.

It establishes deterministic formulas, calculation rules, dependencies, validation logic, and traceability requirements.

Every feature calculation must be reproducible and explainable.

---

# Objectives

The Feature Calculation Engine must

- Produce deterministic calculations.
- Use only validated inputs.
- Preserve traceability.
- Produce reproducible results.
- Prevent duplicate calculations.

---

# Feature Calculation Pipeline

```
Entity JSON

↓

Primitive Feature Calculation

↓

Derived Feature Calculation

↓

Validation

↓

Feature Confidence

↓

Feature JSON
```

---

# Calculation Principles

## Principle 1

Never calculate the same feature twice.

Every feature has exactly one owner.

---

## Principle 2

Every calculation must be deterministic.

Same input

↓

Same output

---

## Principle 3

Every calculation must be explainable.

Every feature stores

- Source Data
- Formula
- Dependencies

---

## Principle 4

Feature calculations never modify Entity JSON.

---

## Principle 5

Derived Features may only use

- Entities
- Primitive Features
- Previously calculated Derived Features

---

# Primitive Feature Calculations

Primitive Features are calculated directly from Entity JSON.

---

## Skill Count

Input

```
Skill Entities
```

Formula

```
Skill Count

=

Number of Skill Entities
```

---

## Company Count

Input

```
Company Entities
```

Formula

```
Company Count

=

Number of Company Entities
```

---

## Project Count

Input

```
Project Entities
```

Formula

```
Project Count

=

Number of Project Entities
```

---

## Certification Count

Input

```
Certification Entities
```

Formula

```
Certification Count

=

Number of Certification Entities
```

---

## Responsibility Count

Input

```
Responsibility Entities
```

Formula

```
Responsibility Count

=

Number of Responsibility Entities
```

---

# Derived Feature Calculations

Derived Features combine multiple primitive features.

---

## Total Years of Experience

Inputs

- Experience Start Dates
- Experience End Dates

Formula

```
Total Experience

=

Sum of all valid employment durations
```

Business Rules

- Ignore overlapping employment periods only if configured.
- Current employment uses evaluation date.

---

## Average Job Duration

Formula

```
Average Job Duration

=

Total Experience

/

Number of Companies
```

---

## Employment Stability

Inputs

- Company Count
- Total Experience
- Career Gap Count

Produces

Employment Stability Indicator

---

## Career Progression

Inputs

- Job Titles
- Employment Timeline

Produces

Career Progression Indicator

---

## Skill Diversity

Inputs

- Technology Count
- Programming Language Count
- Framework Count
- Tool Count

Produces

Skill Diversity Indicator

---

## Resume Completeness

Inputs

- Contact
- Summary
- Experience
- Projects
- Education
- Certifications

Produces

Resume Completeness Indicator

---

## Requirement Density

Inputs

- Required Skills
- Responsibilities
- Certifications

Produces

Requirement Density Indicator

---

# Dependency Rules

Example

```
Experience Entities

↓

Total Experience

↓

Average Job Duration

↓

Employment Stability
```

Dependencies always flow forward.

Circular dependencies are prohibited.

---

# Validation Rules

Validate

- Invalid dates
- Negative durations
- Duplicate entities
- Missing dependencies
- Circular calculations

Return validation errors only.

---

# Calculation Metadata

Every calculated feature records

- Feature ID
- Formula ID
- Input Dependencies
- Calculation Timestamp
- Engine Version

---

# Traceability

Every feature must answer

- Which entities were used?
- Which formula was executed?
- Which intermediate features were used?

---

# Output

Produces

Feature JSON

Containing

- Primitive Features
- Derived Features
- Metadata
- Confidence

---

# Dependencies

Consumes

- Entity JSON

Produces

- Feature JSON

Consumed by

- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring

---

# Related Files

- Book_04_Feature_Engineering.md
- Resume_Feature_Engineering.md
- JD_Feature_Engineering.md
- Derived_Features.md
- Feature_Confidence.md
- Feature_JSON_Specification.md

---

# End of Feature Calculation