# ATS Resume Intelligence Engine

# Entity Normalization

**Version:** 1.0

---

# Purpose

The Entity Normalization module converts extracted entities into a canonical representation while preserving their original values.

Normalization standardizes entity values so that downstream engines can perform reliable and deterministic matching.

This module does not

- Perform Resume ↔ JD Matching
- Calculate ATS Scores
- Perform Semantic Search
- Infer missing entities

---

# Objectives

The module must

- Standardize entity values.
- Preserve original values.
- Remove formatting inconsistencies.
- Create canonical representations.
- Produce deterministic output.

---

# Scope

This module covers

- Skill Normalization
- Technology Normalization
- Company Name Normalization
- Job Title Normalization
- Date Normalization
- Degree Normalization
- Certification Normalization
- URL Normalization
- Phone Number Normalization

This module does not cover

- Semantic Similarity
- Ontology Mapping
- Feature Engineering

---

# Processing Pipeline

```
Entity JSON

↓

Normalization Rules

↓

Canonical Values

↓

Validation

↓

Normalized Entity JSON
```

---

# Normalization Principles

## Preserve Original Value

Every entity must retain the original extracted value.

Example

```
Original

Aws

↓

Canonical

AWS
```

---

## Never Lose Information

Original values are always preserved.

Normalization only adds canonical representations.

---

## Deterministic

The same entity must always normalize to the same canonical value.

---

# Normalization Categories

## Skills

Examples

```
Py Spark

↓

PySpark
```

```
JS

↓

JavaScript
```

---

## Technologies

Examples

```
Apache spark

↓

Apache Spark
```

```
MS SQL

↓

Microsoft SQL Server
```

---

## Cloud Platforms

Examples

```
Amazon Web Services

↓

AWS
```

```
Google Cloud Platform

↓

GCP
```

---

## Databases

Examples

```
Postgre SQL

↓

PostgreSQL
```

```
MS SQL

↓

SQL Server
```

---

## Frameworks

Examples

```
Dot Net

↓

.NET
```

```
Node JS

↓

Node.js
```

---

## Company Names

Examples

```
IBM India Pvt Ltd

↓

IBM
```

```
Amazon Web Services Inc.

↓

Amazon
```

---

## Job Titles

Examples

```
Sr Software Engineer

↓

Senior Software Engineer
```

```
SDE II

↓

Software Development Engineer II
```

---

## Degrees

Examples

```
B.Tech

↓

Bachelor of Technology
```

```
M.S.

↓

Master of Science
```

---

## Certifications

Examples

```
AWS SAA

↓

AWS Certified Solutions Architect – Associate
```

---

## Dates

Normalize to

```
YYYY-MM-DD
```

Preserve original value.

---

## Phone Numbers

Normalize to

```
E.164 Format
```

Example

```
+91 98765 43210
```

---

## URLs

Normalize

- LinkedIn
- GitHub
- Portfolio URLs

---

# Validation Rules

Validate

- Invalid dates
- Invalid URLs
- Invalid phone numbers
- Unknown certifications
- Unknown degree formats

Generate warnings only.

---

# Output Structure

Each normalized entity contains

```
Original Value

↓

Canonical Value

↓

Entity Type

↓

Normalization Status

↓

Confidence
```

---

# Confidence

Normalization confidence indicates how confidently a canonical value was assigned.

Examples

| Original | Canonical | Confidence |
|-----------|-----------|-----------:|
| AWS | AWS | 100% |
| Aws | AWS | 100% |
| Py Spark | PySpark | 98% |
| Postgre SQL | PostgreSQL | 96% |

Normalization confidence is separate from

- Extraction Confidence
- Matching Confidence

---

# Rules

Rule 1

Never overwrite original values.

---

Rule 2

Canonical values must be deterministic.

---

Rule 3

Unknown entities remain unchanged.

---

Rule 4

Normalization must be reversible.

Original values must always be recoverable.

---

# Dependencies

Consumes

- Resume Entity JSON
- JD Entity JSON

Produces

- Normalized Entity JSON

Consumed by

- Feature Engineering
- Hybrid Knowledge Layer

---

# Related Files

- Book_03_Entity_Extraction.md
- Resume_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Confidence.md
- Entity_Relationships.md
- Entity_JSON_Specification.md

---

# End of Entity Normalization