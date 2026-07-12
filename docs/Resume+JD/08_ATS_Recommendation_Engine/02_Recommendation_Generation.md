# ATS Resume Intelligence Engine

# Recommendation Generation

**Version:** 1.0

---

# Purpose

The Recommendation Generation Engine transforms Gap Objects into actionable Resume improvement recommendations.

Its responsibility is to convert identified gaps into clear, structured, evidence-backed guidance that can be consumed by downstream systems.

The Recommendation Generation Engine never rewrites Resume content.

It never generates fabricated experience or skills.

---

# Objectives

The Recommendation Generation Engine must

- Transform Gap Objects into Recommendations.
- Preserve explainability.
- Preserve traceability.
- Generate deterministic recommendations.
- Produce Recommendation Objects.

---

# Scope

This module covers

- Requirement Recommendations
- Evidence Recommendations
- Coverage Recommendations
- Quality Recommendations
- ATS Compatibility Recommendations

This module does not cover

- Resume Rewriting
- Prompt Engineering
- ATS Scoring
- Resume Matching
- LLM Integration

---

# Inputs

Consumes

- Gap Objects
- Evidence JSON
- Score JSON

Produced by

- Gap Analysis
- Evidence Intelligence
- ATS Scoring

---

# Outputs

Produces

- Recommendation Objects

Consumed by

- Recommendation Prioritization
- Score Impact Estimation
- Recommendation Validation

---

# Processing Pipeline

```
Gap Objects

↓

Gap Classification

↓

Recommendation Mapping

↓

Recommendation Generation

↓

Recommendation Objects
```

---

# Recommendation Philosophy

The Recommendation Generation Engine answers one question.

> "What should be improved to address this specific gap?"

Recommendations describe **what** should improve.

They never describe **how** to rewrite the Resume.

That responsibility belongs to the Resume Intelligence repository.

---

# Recommendation Categories

## Requirement Recommendation

Generated from

Requirement Gaps

Examples

- Add missing technical skill.
- Add missing certification.
- Add missing responsibility.
- Add missing project experience.

---

## Evidence Recommendation

Generated from

Evidence Gaps

Examples

- Strengthen supporting project.
- Add experience demonstrating the claimed skill.
- Provide measurable achievements.

---

## Coverage Recommendation

Generated from

Coverage Gaps

Examples

- Expand cloud experience.
- Improve leadership examples.
- Cover additional responsibilities.

---

## Quality Recommendation

Generated from

Quality Gaps

Examples

- Improve Professional Summary.
- Strengthen Experience bullets.
- Add measurable outcomes.
- Improve project descriptions.

---

## ATS Compatibility Recommendation

Generated from

ATS Compatibility Gaps

Examples

- Remove tables.
- Remove images.
- Use standard section headings.
- Simplify Resume formatting.

---

# Recommendation Object

Every Recommendation contains

- Recommendation ID
- Recommendation Category
- Priority (assigned later)
- Related Gap
- Related Requirement
- Related Resume Section
- Recommendation Title
- Recommendation Description
- Supporting Evidence
- Metadata

---

# Recommendation Rules

## Rule 1

Every Recommendation must reference exactly one Gap Object.

---

## Rule 2

Every Recommendation must preserve traceability to Evidence.

---

## Rule 3

Recommendations must never invent candidate experience.

---

## Rule 4

Recommendations must never recommend false skills.

---

## Rule 5

Recommendations must never modify Score JSON.

---

## Rule 6

Recommendations must never modify Evidence JSON.

---

## Rule 7

Recommendation generation must always be deterministic.

---

# Example

```
Gap

Missing Apache Spark

↓

Recommendation

Add Apache Spark experience if applicable.

↓

Evidence

Requirement #14

↓

Category

Requirement Recommendation
```

---

Another Example

```
Gap

Weak Project Evidence

↓

Recommendation

Strengthen project descriptions with measurable outcomes.

↓

Category

Quality Recommendation
```

---

# Validation

Validate

- Missing Gap Reference
- Missing Requirement Reference
- Missing Evidence Reference
- Duplicate Recommendations
- Invalid Recommendation Category

Return validation failures only.

---

# Recommendation Output

Produces

- Recommendation Objects
- Recommendation Summary
- Recommendation Categories

---

# Design Principles

## Evidence Driven

Recommendations originate only from validated Gap Objects.

---

## Deterministic

The same Gap Object always generates the same Recommendation.

---

## Explainable

Every Recommendation must explain why it exists.

---

## Independent

Each Recommendation must be independently actionable.

---

## Truthful

Recommendations must never encourage fabrication of skills, projects, education, certifications, or experience.

---

# Dependencies

Consumes

- Gap Objects
- Evidence JSON
- Score JSON

Produces

- Recommendation Objects

Consumed by

- Recommendation Prioritization
- Score Impact Estimation
- Recommendation Validation

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- Gap_Analysis.md
- Recommendation_Prioritization.md
- Score_Impact_Estimation.md
- Recommendation_Validation.md
- Recommendation_JSON_Specification.md
- Recommendation_API_Contract.md

---

# End of Recommendation Generation