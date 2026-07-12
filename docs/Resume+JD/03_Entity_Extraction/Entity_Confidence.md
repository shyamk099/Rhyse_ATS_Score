# ATS Resume Intelligence Engine

# Entity Confidence

**Version:** 1.0

---

# Purpose

The Entity Confidence module measures the reliability of every extracted entity.

Entity Confidence indicates how confidently the system believes an entity was correctly identified and classified.

Entity Confidence never changes the ATS Score.

---

# Objectives

The module must

- Measure extraction reliability.
- Measure normalization reliability.
- Preserve confidence throughout the pipeline.
- Produce deterministic confidence values.

---

# Scope

This module covers

- Extraction Confidence
- Normalization Confidence
- Overall Entity Confidence

This module does not cover

- Matching Confidence
- Semantic Confidence
- ATS Scoring

---

# Processing Pipeline

```
Resume / JD

↓

Entity Extraction

↓

Extraction Confidence

↓

Entity Normalization

↓

Normalization Confidence

↓

Entity Confidence

↓

Entity JSON
```

---

# Confidence Philosophy

Entity Confidence answers one question.

> "How confident are we that this extracted entity is correct?"

It does not answer

> "How well does this entity match the Job Description?"

---

# Confidence Components

Every entity contains three confidence values.

## 1. Extraction Confidence

Measures how confidently the parser extracted the entity.

Examples

- Clear section headings
- Recognized patterns
- OCR quality
- Parsing success

---

## 2. Normalization Confidence

Measures how confidently the original value was normalized.

Examples

```
Aws

↓

AWS

100%
```

```
Py Spark

↓

PySpark

98%
```

---

## 3. Overall Entity Confidence

Represents the combined confidence of the entity.

```
Overall Confidence

=

Extraction Confidence

+

Normalization Confidence

↓

Weighted Result
```

The weighting strategy is implementation-specific and must remain deterministic.

---

# Confidence Levels

| Confidence | Level |
|------------|--------|
| 95–100 | Very High |
| 85–94 | High |
| 70–84 | Medium |
| 50–69 | Low |
| Below 50 | Very Low |

---

# Examples

## Example 1

```
Original

Python

↓

Extraction

100%

↓

Normalization

100%

↓

Overall

100%
```

---

## Example 2

```
Original

Postgre SQL

↓

Extraction

98%

↓

Normalization

95%

↓

Overall

96%
```

---

## Example 3

```
Original

Aws

↓

Extraction

96%

↓

Normalization

100%

↓

Overall

98%
```

---

# Rules

## Rule 1

Confidence must always be deterministic.

---

## Rule 2

Confidence must never modify entity values.

---

## Rule 3

Confidence must never modify ATS scores.

---

## Rule 4

Confidence values must be preserved throughout the pipeline.

---

## Rule 5

Confidence calculations must be reproducible.

---

# Output

Every entity contains

```
Entity

↓

Extraction Confidence

↓

Normalization Confidence

↓

Overall Entity Confidence
```

---

# Dependencies

Consumes

- Resume Entity JSON
- JD Entity JSON
- Normalized Entity JSON

Produces

- Entity Confidence

Consumed by

- Feature Engineering
- Evidence Intelligence
- Confidence Aggregator

---

# Related Files

- Book_03_Entity_Extraction.md
- Resume_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Relationships.md
- Entity_JSON_Specification.md

---

# End of Entity Confidence