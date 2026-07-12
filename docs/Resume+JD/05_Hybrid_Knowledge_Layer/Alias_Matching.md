# ATS Resume Intelligence Engine

# Alias Matching

**Version:** 1.0

---

# Purpose

The Alias Matching Engine determines whether two features represent the same business concept through predefined aliases.

Unlike Exact Matching, Alias Matching uses a controlled Alias Dictionary to identify officially recognized alternate names.

Alias Matching executes only when Exact Matching fails.

If Alias Matching succeeds, no lower-priority strategy is executed for that feature pair.

---

# Objectives

The Alias Matching Engine must

- Resolve official aliases.
- Resolve abbreviations.
- Resolve common technology names.
- Produce deterministic matches.
- Generate Match Objects.

---

# Scope

This module covers

- Technology Aliases
- Programming Language Aliases
- Framework Aliases
- Database Aliases
- Cloud Platform Aliases
- Certification Aliases
- Tool Aliases
- Job Title Aliases

This module does not cover

- Typographical Errors
- Ontology Relationships
- Semantic Similarity

---

# Inputs

Consumes

- Resume Feature JSON
- JD Feature JSON
- Alias Dictionary

Produced by

- Feature Engineering

---

# Outputs

Produces

- Alias Match Objects

Consumed by

- Matching Pipeline

---

# Processing Pipeline

```
Resume Feature

+

JD Feature

↓

Exact Match Failed

↓

Alias Lookup

↓

Alias Validation

↓

Match Confidence

↓

Match Object
```

---

# Matching Rule

Two features are considered an Alias Match only if both resolve to the same canonical value using the Alias Dictionary.

---

# Examples

## Cloud Platform

```
Resume

AWS

↓

JD

Amazon Web Services

↓

Alias Match
```

---

## Programming Language

```
Resume

JS

↓

JD

JavaScript

↓

Alias Match
```

---

## Framework

```
Resume

Dot Net

↓

JD

.NET

↓

Alias Match
```

---

## Database

```
Resume

MS SQL

↓

JD

Microsoft SQL Server

↓

Alias Match
```

---

## Certification

```
Resume

AWS SAA

↓

JD

AWS Certified Solutions Architect – Associate

↓

Alias Match
```

---

# Non-Matches

```
Resume

Apache Spark

↓

JD

Apache Kafka
```

Not an Alias Match.

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

# Alias Dictionary

The Alias Dictionary is the only source used for alias resolution.

Each alias maps to exactly one canonical value.

Example

```
JS

↓

JavaScript
```

```
Amazon Web Services

↓

AWS
```

```
Dot Net

↓

.NET
```

The Alias Dictionary is version controlled.

---

# Validation Rules

Validate

- Missing Canonical Value
- Invalid Alias
- Duplicate Alias Entries
- Conflicting Canonical Values

Return validation failures only.

---

# Match Confidence

Alias Matching produces a high confidence because the relationship is explicitly defined.

Confidence is determined by

- Alias Dictionary Match
- Canonical Value Match
- Entity Type Match

The confidence calculation is defined in

Matching_Confidence.md

---

# Match Object

Each successful match records

- Resume Feature ID
- JD Feature ID
- Alias Used
- Canonical Value
- Matching Strategy
- Match Reason
- Confidence

---

# Rules

## Rule 1

Only the Alias Dictionary may resolve aliases.

---

## Rule 2

LLMs must never generate aliases.

---

## Rule 3

Alias Matching must be deterministic.

---

## Rule 4

A successful Alias Match terminates further matching for that feature pair.

---

## Rule 5

Every successful Alias Match produces exactly one Match Object.

---

# Dependencies

Consumes

- Resume Feature JSON
- JD Feature JSON
- Alias Dictionary

Produces

- Match Object

Consumed by

- Matching Pipeline
- Evidence Intelligence

---

# Related Files

- Book_05_Hybrid_Knowledge_Layer.md
- Exact_Matching.md
- Fuzzy_Matching.md
- Ontology_Matching.md
- Semantic_Matching.md
- Alias_Dictionary.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Match_JSON_Specification.md

---

# End of Alias Matching