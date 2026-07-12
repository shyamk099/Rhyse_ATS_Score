# ATS Resume Intelligence Engine

# Ontology Matching

**Version:** 1.0

---

# Purpose

The Ontology Matching Engine determines whether Resume and Job Description features are related through a predefined Technology Ontology.

Unlike Exact, Alias, and Fuzzy Matching, Ontology Matching does not compare text.

Instead, it compares business relationships stored inside the ontology graph.

Ontology Matching executes only after

- Exact Matching
- Alias Matching
- Fuzzy Matching

have all failed.

If Ontology Matching succeeds, Semantic Matching is not executed for that feature pair.

---

# Objectives

The Ontology Matching Engine must

- Discover ontology relationships.
- Traverse the technology graph.
- Produce deterministic matches.
- Generate explainable Match Objects.
- Record ontology evidence.

---

# Scope

This module covers

- Technology Relationships
- Framework Relationships
- Cloud Relationships
- Database Relationships
- Tool Relationships
- Platform Relationships

This module does not cover

- Alias Resolution
- Typographical Errors
- Semantic Similarity
- LLM Reasoning

---

# Inputs

Consumes

- Resume Feature JSON
- JD Feature JSON
- Technology Ontology

Produced by

- Feature Engineering

---

# Outputs

Produces

- Ontology Match Objects

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

Ontology Lookup

↓

Relationship Validation

↓

Match Confidence

↓

Match Object
```

---

# Matching Philosophy

Ontology Matching determines whether two entities are connected through an explicit relationship.

Relationships are defined in the Technology Ontology.

No embeddings are used.

No language models are used.

---

# Supported Relationship Types

Examples

- runs_on
- belongs_to
- part_of
- framework_of
- database_of
- service_of
- managed_service_of
- programming_language_of
- cloud_provider_of
- tool_for

The relationship catalog is version controlled.

---

# Examples

## Cloud Service

```
Resume

Amazon EMR

↓

runs_on

↓

AWS

↓

JD

AWS

↓

Ontology Match
```

---

## Framework

```
Resume

ASP.NET Core

↓

framework_of

↓

.NET

↓

JD

.NET

↓

Ontology Match
```

---

## Database Service

```
Resume

Amazon RDS

↓

managed_service_of

↓

PostgreSQL

↓

JD

PostgreSQL

↓

Ontology Match
```

---

## Container Service

```
Resume

Amazon ECS

↓

container_service_of

↓

Docker

↓

JD

Docker

↓

Ontology Match
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

Postgre SQL

↓

JD

PostgreSQL
```

Handled by Fuzzy Matching.

---

```
Resume

PySpark

↓

JD

Apache Spark
```

Handled by Semantic Matching (if applicable).

---

# Ontology Rules

## Rule 1

Only predefined ontology relationships may be used.

---

## Rule 2

No relationship may be inferred dynamically.

---

## Rule 3

Ontology relationships are directional.

Example

```
Amazon EMR

↓

runs_on

↓

AWS
```

Direction must be preserved.

---

## Rule 4

Ontology traversal depth is configurable and version controlled.

---

## Rule 5

The ontology is immutable during matching.

---

# Relationship Validation

Validate

- Missing Nodes
- Invalid Relationships
- Invalid Edge Direction
- Missing Canonical Entities
- Circular References

Return validation failures only.

---

# Match Confidence

Ontology Matching confidence depends on

- Relationship Validity
- Traversal Depth
- Relationship Type
- Node Confidence

The confidence calculation is defined in

Matching_Confidence.md

---

# Match Object

Each successful match records

- Resume Feature ID
- JD Feature ID
- Source Node
- Target Node
- Relationship Type
- Traversal Path
- Matching Strategy
- Match Reason
- Confidence

---

# Rules

## Rule 1

Only ontology relationships may produce Ontology Matches.

---

## Rule 2

Ontology Matching must always be deterministic.

---

## Rule 3

Ontology Matching never modifies Feature JSON.

---

## Rule 4

A successful Ontology Match terminates further matching for that feature pair.

---

## Rule 5

Every successful Ontology Match produces exactly one Match Object.

---

# Dependencies

Consumes

- Resume Feature JSON
- JD Feature JSON
- Technology Ontology

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
- Semantic_Matching.md
- Technology_Ontology.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Match_JSON_Specification.md

---

# End of Ontology Matching