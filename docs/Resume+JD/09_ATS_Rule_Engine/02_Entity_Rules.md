# ATS Resume Intelligence Engine

# Entity Rules

**Version:** 1.0

---

# Purpose

The Entity Rules Engine defines the configurable business rules used by the Entity Intelligence Engine.

Entity Rules determine how extracted Resume entities are validated, normalized, classified, and resolved.

Entity Rules never extract entities.

They only define how extracted entities should be interpreted.

---

# Objectives

The Entity Rules Engine must

- Configure entity normalization.
- Configure alias resolution.
- Configure ontology mapping.
- Configure confidence thresholds.
- Configure entity validation.
- Preserve deterministic entity processing.

---

# Scope

This module covers

- Entity Categories
- Alias Rules
- Normalization Rules
- Ontology Rules
- Confidence Rules
- Validation Rules

This module does not cover

- Resume Parsing
- Entity Extraction
- Feature Engineering

---

# Inputs

Consumes

- Entity Rule Configuration

Produced by

- ATS Administrator
- Business Configuration

---

# Outputs

Produces

- Runtime Entity Rules

Consumed by

- Entity Intelligence Engine

---

# Rule Philosophy

Entity Rules answer one question.

> "How should extracted entities be interpreted?"

The Entity Intelligence Engine consumes these rules during execution.

---

# Processing Pipeline

```
Entity Rule Configuration

↓

Rule Loader

↓

Rule Validation

↓

Runtime Entity Rules

↓

Entity Intelligence Engine
```

---

# Rule Categories

## Entity Categories

Defines supported entity types.

Examples

- Skill
- Tool
- Framework
- Programming Language
- Database
- Cloud Platform
- Certification
- Degree
- Company
- Job Title
- Domain

---

## Alias Rules

Defines alternate names for the same entity.

Example

```
PySpark

↓

Apache Spark
```

```
MS SQL

↓

Microsoft SQL Server
```

```
GCP

↓

Google Cloud Platform
```

Alias mappings are configurable.

---

## Normalization Rules

Defines canonical names.

Example

```
Spark SQL

↓

Apache Spark
```

```
AWS EC2

↓

Amazon EC2
```

All downstream engines consume normalized entities.

---

## Ontology Rules

Defines ontology mappings.

Example

```
Apache Spark

↓

Distributed Computing

↓

Big Data

↓

Data Engineering
```

Ontology relationships are configurable.

---

## Confidence Rules

Defines minimum confidence for accepting an entity.

Example

```
Minimum Confidence

0.90
```

Entities below threshold may be rejected or flagged.

---

## Validation Rules

Defines

- Duplicate entities
- Invalid entities
- Unknown entities
- Deprecated entities

Validation behavior is configurable.

---

# Rule Lifecycle

```
Configuration

↓

Validation

↓

Activation

↓

Entity Processing
```

---

# Rule Validation

Validate

- Missing Categories
- Duplicate Aliases
- Circular Alias References
- Invalid Ontology Links
- Invalid Confidence Values

Only validated rules become active.

---

# Design Principles

## Configurable

Entity behavior must never be hardcoded.

---

## Deterministic

The same entity with the same rules must always normalize identically.

---

## Versioned

Every Entity Rule set has a version.

---

## Immutable

Rules cannot change during execution.

---

## Traceable

Every entity records the Entity Rule Version used.

---

# Example Configuration

```yaml
entity:

  confidence:
    minimum: 0.90

  aliases:

    pyspark:
      canonical: apache_spark

    spark_sql:
      canonical: apache_spark

    gcp:
      canonical: google_cloud_platform

  ontology:

    apache_spark:
      parent: distributed_computing

    distributed_computing:
      parent: data_engineering
```

---

# Rule Rules

## Rule 1

Alias mappings must always resolve to one canonical entity.

---

## Rule 2

Ontology relationships must never contain cycles.

---

## Rule 3

Rules are read-only during execution.

---

## Rule 4

Every entity normalization records the Rule Version.

---

## Rule 5

Runtime engines cannot modify entity rules.

---

# Dependencies

Consumes

- Entity Rule Configuration

Produces

- Runtime Entity Rules

Consumed by

- Entity Intelligence Engine

---

# Related Files

- Book_09_ATS_Rule_Engine.md
- Parser_Rules.md
- Feature_Rules.md
- Matching_Rules.md
- Rule_JSON_Specification.md

---

# End of Entity Rules