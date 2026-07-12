# ATS Resume Intelligence Engine

# Integrity Penalty

**Version:** 1.0

---

# Purpose

The Integrity Penalty Engine detects Resume manipulation techniques that artificially inflate ATS scores.

Its responsibility is to identify deceptive Resume practices and apply bounded penalties to the Raw ATS Score.

The Integrity Penalty Engine never performs Resume matching.

---

# Objectives

The Integrity Penalty Engine must

- Detect Resume manipulation.
- Detect keyword stuffing.
- Detect hidden keywords.
- Detect duplicate keyword abuse.
- Detect artificial skill inflation.
- Apply deterministic penalties.

---

# Scope

This module covers

- Keyword Stuffing
- Hidden Text
- Duplicate Keywords
- Artificial Skill Inflation
- Section Abuse
- Resume Manipulation

This module does not cover

- Resume Quality
- ATS Compatibility
- Resume–JD Matching
- Resume Optimization

---

# Inputs

Consumes

- Resume Feature JSON
- Evidence JSON

Produced by

- Feature Engineering
- Evidence Intelligence

---

# Outputs

Produces

- Integrity Penalty

Consumed by

- Weighted Scoring Engine

---

# Design Philosophy

The Integrity Penalty answers one question.

> "Is the Resume attempting to manipulate the ATS Score?"

Integrity Penalty is the only negative scoring component.

---

# Processing Pipeline

```
Resume Feature JSON

+

Evidence JSON

↓

Manipulation Detection

↓

Violation Detection

↓

Penalty Calculation

↓

Bound Validation

↓

Integrity Penalty
```

---

# Violation Categories

## Keyword Stuffing

Detects

- Excessive keyword repetition
- Artificial keyword density
- Repeated skill lists

Example

```
Python

Python

Python

Python

Python

Python
```

---

## Hidden Keywords

Detects

- White text
- Invisible text
- Zero-size fonts
- Hidden layers

---

## Duplicate Keyword Abuse

Detects

- Duplicate technical skills
- Duplicate certifications
- Duplicate project keywords

---

## Artificial Skill Inflation

Detects

Examples

- Listing unrelated skills
- Listing unsupported technologies
- Listing tools with no supporting evidence

---

## Section Abuse

Detects

- Extremely long Skills sections
- Artificially repeated Experience bullets
- Duplicate Projects

---

# Penalty Rules

Each violation records

- Violation ID
- Violation Type
- Severity
- Evidence
- Penalty Value

---

# Severity Levels

- Low
- Medium
- High
- Critical

Severity is determined by configurable business rules.

---

# Penalty Boundaries

The Integrity Penalty is bounded.

Rules

- Penalty cannot exceed configured maximum.
- Final ATS Score cannot fall below configured minimum.
- Multiple penalties are cumulative up to the configured cap.

---

# Example

```
Keyword Stuffing

↓

High Severity

↓

Penalty

6.5
```

---

Another Example

```
Hidden White Text

↓

Critical

↓

Penalty

10
```

---

# Validation

Validate

- Duplicate Violations
- Invalid Penalty Values
- Missing Evidence
- Missing Severity
- Invalid Penalty Bounds

Return validation failures only.

---

# Rules

## Rule 1

Every penalty must reference supporting Evidence.

---

## Rule 2

Integrity Penalty must always be deterministic.

---

## Rule 3

Penalties are applied only once per violation.

---

## Rule 4

Penalty values are configurable.

---

## Rule 5

Penalty values are version controlled.

---

## Rule 6

Penalty application must preserve traceability.

---

## Rule 7

Penalty never modifies Evidence JSON.

---

# Penalty Output

Produces

- Integrity Penalty
- Violation Summary
- Severity Summary
- Penalty Breakdown

---

# Dependencies

Consumes

- Resume Feature JSON
- Evidence JSON

Produces

- Integrity Penalty

Consumed by

- Weighted Scoring Engine

---

# Related Files

- Book_07_ATS_Scoring.md
- Weighted_Scoring_Engine.md
- Score_Calibration.md
- Score_JSON_Specification.md

---

# End of Integrity Penalty