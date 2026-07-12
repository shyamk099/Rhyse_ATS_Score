# ATS Resume Intelligence Engine

# Semantic Matching

**Version:** 1.0

---

# Purpose

The Semantic Matching Engine determines whether Resume and Job Description features represent the same business concept using semantic similarity.

Unlike Exact, Alias, Fuzzy, and Ontology Matching, Semantic Matching understands contextual meaning rather than textual similarity or predefined relationships.

Semantic Matching executes only after all previous matching strategies fail.

Semantic Matching is the final strategy in the Hybrid Knowledge Layer.

---

# Objectives

The Semantic Matching Engine must

- Detect contextual similarity.
- Compare semantic meaning.
- Produce explainable matches.
- Generate deterministic Match Objects.
- Record semantic evidence.

---

# Scope

This module covers

- Embedding Similarity
- Contextual Similarity
- Business Meaning Similarity
- Skill Context Matching
- Responsibility Context Matching

This module does not cover

- Exact Matching
- Alias Matching
- Fuzzy Matching
- Ontology Relationships

---

# Inputs

Consumes

- Resume Feature JSON
- JD Feature JSON
- Embedding Model

Produced by

- Feature Engineering

---

# Outputs

Produces

- Semantic Match Objects

Consumed by

- Matching Pipeline
- Evidence Intelligence

---

# Processing Pipeline

```
Resume Feature

+

JD Feature

↓

Exact Match Failed

↓

Alias Match Failed

↓

Fuzzy Match Failed

↓

Ontology Match Failed

↓

Embedding Generation

↓

Similarity Calculation

↓

Threshold Validation

↓

Semantic Match

↓

Match Confidence

↓

Match Object
```

---

# Matching Philosophy

Semantic Matching determines whether two features have the same business meaning.

Similarity is based on embeddings rather than text equality.

No ontology traversal is performed.

No alias lookup is performed.

---

# Semantic Examples

## Skill Context

```
Resume

ETL Pipeline Development

↓

JD

Data Pipeline Development

↓

Semantic Match
```

---

## Responsibility

```
Resume

Designed REST APIs

↓

JD

Built Backend APIs

↓

Semantic Match
```

---

## Cloud Experience

```
Resume

Managed AWS Infrastructure

↓

JD

Cloud Infrastructure Management

↓

Semantic Match
```

---

## Leadership

```
Resume

Mentored Junior Engineers

↓

JD

Technical Leadership

↓

Semantic Match
```

---

# Non-Matches

```
Resume

AWS

↓

JD

Amazon Web Services
```

Handled by Alias Matching.

---

```
Resume

Amazon EMR

↓

JD

AWS
```

Handled by Ontology Matching.

---

```
Resume

Postgre SQL

↓

JD

PostgreSQL
```

Handled by Fuzzy Matching.

---

# Embedding Rules

Embeddings must

- Be version controlled.
- Be deterministic for identical inputs.
- Use the same embedding model for Resume and JD.

Embedding model changes require a new Algorithm Version.

---

# Similarity Rules

Semantic similarity is evaluated using embedding vectors.

A match is produced only when

- Similarity exceeds the configured threshold.
- Business validation succeeds.

Thresholds are version controlled.

---

# Validation Rules

Validate

- Missing embeddings
- Invalid vectors
- Threshold failures
- Unsupported feature types

Return validation failures only.

---

# Match Confidence

Semantic Matching confidence depends on

- Embedding Similarity
- Validation Success
- Threshold Margin
- Feature Consistency

Confidence calculation is defined in

Matching_Confidence.md

---

# Match Object

Each successful match records

- Resume Feature ID
- JD Feature ID
- Embedding Model Version
- Similarity Score
- Threshold
- Matching Strategy
- Match Reason
- Confidence

---

# Rules

## Rule 1

Semantic Matching executes only after all previous strategies fail.

---

## Rule 2

Semantic Matching never overrides a previous successful match.

---

## Rule 3

Semantic Matching must be deterministic for the same model version.

---

## Rule 4

Semantic Matching never modifies Feature JSON.

---

## Rule 5

Every successful Semantic Match produces exactly one Match Object.

---

# Dependencies

Consumes

- Resume Feature JSON
- JD Feature JSON
- Embedding Model

Produces

- Match Object

Consumed by

- Matching Pipeline
- Evidence Intelligence

---

# Related Files

- Book_05_Hybrid_Knowledge_Layer.md
- Exact_Matching.md
- Alias_Matching.md
- Fuzzy_Matching.md
- Ontology_Matching.md
- Technology_Ontology.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Match_JSON_Specification.md

---

# End of Semantic Matching