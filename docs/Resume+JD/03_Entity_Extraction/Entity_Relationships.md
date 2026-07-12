# ATS Resume Intelligence Engine

# Entity Relationships

**Version:** 1.0

---

# Purpose

The Entity Relationships module identifies and records relationships between extracted entities.

Relationships provide contextual information that cannot be represented by individual entities alone.

This module does not

- Perform Resume ↔ JD Matching
- Calculate ATS Scores
- Perform Semantic Search
- Generate Evidence

---

# Objectives

The module must

- Connect related entities.
- Preserve relationship context.
- Support downstream feature engineering.
- Produce deterministic relationship objects.

---

# Scope

This module covers

- Resume Relationships
- Job Description Relationships
- Cross-Entity References

This module does not cover

- Resume ↔ JD Relationships
- Ontology Relationships
- Semantic Relationships

---

# Processing Pipeline

```
Entity JSON

↓

Relationship Discovery

↓

Relationship Validation

↓

Relationship JSON
```

---

# Relationship Philosophy

An entity represents **what** exists.

A relationship represents **how entities are connected**.

Example

```
Python

↓

used_in

↓

Project A
```

Without the relationship

```
Python

Project A
```

are only independent entities.

---

# Relationship Types

## Experience → Company

Example

```
Software Engineer

↓

worked_at

↓

Microsoft
```

---

## Experience → Technology

Example

```
Data Engineer

↓

used

↓

Apache Spark
```

---

## Project → Technology

Example

```
Fraud Detection Platform

↓

built_with

↓

Kafka
```

---

## Project → Responsibility

Example

```
Customer Analytics

↓

includes

↓

Developed ETL Pipelines
```

---

## Certification → Organization

Example

```
AWS Certified Solutions Architect

↓

issued_by

↓

Amazon Web Services
```

---

## Education → Institution

Example

```
Bachelor of Technology

↓

awarded_by

↓

Anna University
```

---

## Skill → Experience

Example

```
Python

↓

demonstrated_in

↓

Senior Data Engineer
```

---

## Skill → Project

Example

```
Docker

↓

used_in

↓

Microservices Platform
```

---

## Technology → Cloud Platform

Example

```
EMR

↓

runs_on

↓

AWS
```

---

## Responsibility → Technology

Example

```
Build ETL Pipelines

↓

requires

↓

Apache Spark
```

---

# Relationship Object

Each relationship contains

- Relationship ID
- Source Entity ID
- Target Entity ID
- Relationship Type
- Source Section
- Confidence

---

# Relationship Rules

## Rule 1

Relationships connect existing entities only.

No new entities may be created.

---

## Rule 2

Relationships must be deterministic.

---

## Rule 3

Relationships never modify entity values.

---

## Rule 4

Every relationship references valid Entity IDs.

---

## Rule 5

Relationships preserve provenance.

The originating section and document location must be retained.

---

# Validation

Validate

- Missing Entity IDs
- Invalid Relationship Types
- Circular Self References
- Orphan Relationships

Return warnings only.

---

# Output

Produces

Relationship JSON

```
Relationship

↓

Source Entity

↓

Relationship Type

↓

Target Entity

↓

Confidence
```

---

# Dependencies

Consumes

- Resume Entity JSON
- JD Entity JSON

Produces

- Relationship JSON

Consumed by

- Feature Engineering
- Evidence Intelligence

---

# Related Files

- Book_03_Entity_Extraction.md
- Resume_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Confidence.md
- Entity_JSON_Specification.md

---

# End of Entity Relationships