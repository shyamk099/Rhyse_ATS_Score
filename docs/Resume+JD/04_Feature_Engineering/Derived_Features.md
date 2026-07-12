# ATS Resume Intelligence Engine

# Derived Features

**Version:** 1.0

---

# Purpose

This document defines every derived feature used throughout the ATS Resume Intelligence Engine.

A derived feature is a measurable business attribute calculated from one or more entities or primitive features.

Derived features provide higher-level intelligence for matching, evidence generation, and ATS scoring.

This document is the central feature catalog used by both Resume Feature Engineering and JD Feature Engineering.

---

# Objectives

The Derived Feature Engine must

- Produce deterministic features.
- Produce explainable calculations.
- Avoid duplicate calculations.
- Create reusable business features.
- Maintain feature traceability.

---

# Feature Hierarchy

```
Entities

↓

Primitive Features

↓

Derived Features

↓

Feature JSON

↓

Hybrid Knowledge Layer
```

---

# Primitive Features

Primitive features are calculated directly from entities.

Examples

- Skill Count
- Company Count
- Project Count
- Certification Count
- Experience Count
- Education Count
- Responsibility Count

Primitive features never depend on other features.

---

# Derived Features

Derived features are calculated using one or more primitive features.

Examples

- Career Progression
- Employment Stability
- Skill Diversity
- Resume Completeness
- Requirement Density

---

# Feature Categories

---

## Experience Features

Examples

- Total Years of Experience
- Average Job Duration
- Longest Employment
- Shortest Employment
- Career Gap Count
- Career Gap Duration
- Career Progression
- Promotion Count
- Employment Stability

---

## Skill Features

Examples

- Total Skills
- Technical Skill Density
- Soft Skill Density
- Technology Diversity
- Programming Language Diversity
- Cloud Technology Diversity
- Database Diversity
- Tool Diversity
- Skill Distribution
- Skill Frequency

---

## Project Features

Examples

- Total Projects
- Average Technologies per Project
- Project Complexity
- Leadership Projects
- Enterprise Projects
- Open Source Projects
- Cross-Functional Projects

---

## Education Features

Examples

- Highest Education Level
- Degree Diversity
- Academic Progression

---

## Certification Features

Examples

- Certification Count
- Vendor Diversity
- Cloud Certification Count
- Technology Certification Count

---

## Responsibility Features

Examples

- Leadership Responsibility Count
- Development Responsibility Count
- Architecture Responsibility Count
- Management Responsibility Count

---

## Resume Quality Features

Examples

- Resume Completeness
- Contact Completeness
- Experience Completeness
- Project Completeness
- Education Completeness
- Certification Completeness

---

## Job Requirement Features

Examples

- Mandatory Requirement Density
- Preferred Requirement Density
- Skill Density
- Responsibility Density
- Technology Density

---

# Feature Rules

## Rule 1

Every derived feature must be traceable.

---

## Rule 2

Every derived feature must be reproducible.

---

## Rule 3

Derived features may depend only on

- Entities
- Primitive Features
- Previously defined Derived Features

Circular dependencies are not allowed.

---

## Rule 4

Every feature must have one owner.

No feature may be calculated by multiple engines.

---

## Rule 5

Features must never modify Entity JSON.

---

# Feature Dependency

Example

```
Experience Entities

↓

Primitive Feature

↓

Company Count

↓

Derived Feature

↓

Employment Stability
```

---

Another Example

```
Skill Entities

↓

Primitive Feature

↓

Technology Count

↓

Derived Feature

↓

Technology Diversity
```

---

# Feature Metadata

Every derived feature records

- Feature ID
- Feature Name
- Feature Category
- Source Features
- Calculation Method
- Confidence
- Version

---

# Validation

Validate

- Missing dependencies
- Circular dependencies
- Invalid feature references
- Duplicate feature identifiers

Return validation errors only.

---

# Dependencies

Consumes

- Resume Feature Engineering
- JD Feature Engineering

Produces

- Derived Feature Library

Consumed by

- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring

---

# Related Files

- Book_04_Feature_Engineering.md
- Resume_Feature_Engineering.md
- JD_Feature_Engineering.md
- Feature_Calculation.md
- Feature_Confidence.md
- Feature_JSON_Specification.md

---

# End of Derived Features