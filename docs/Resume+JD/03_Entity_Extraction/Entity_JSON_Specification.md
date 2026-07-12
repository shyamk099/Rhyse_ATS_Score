# ATS Resume Intelligence Engine

# Entity JSON Specification

**Version:** 1.0

---

# Purpose

This document defines the canonical Entity JSON model used throughout the ATS Resume Intelligence Engine.

The Entity JSON is the primary data contract between Entity Extraction and all downstream intelligence modules.

Every entity extracted from a Resume or Job Description must conform to this specification.

---

# Design Principles

The Entity JSON follows these principles.

- Deterministic
- Immutable
- Extensible
- Explainable
- Version Controlled
- Source Preserving

---

# Processing Flow

```
Resume / JD

↓

Entity Extraction

↓

Normalization

↓

Confidence

↓

Relationships

↓

Entity JSON

↓

Feature Engineering
```

---

# Entity Structure

Every entity follows the same structure regardless of entity type.

```json
{
  "entity_id": "",
  "entity_type": "",
  "original_value": "",
  "canonical_value": "",
  "normalized": false,
  "source": {},
  "confidence": {},
  "relationships": [],
  "metadata": {}
}
```

---

# Entity Fields

## entity_id

Unique identifier.

Example

```
ENT-000001
```

---

## entity_type

Examples

- Skill
- Technology
- Programming Language
- Framework
- Tool
- Cloud Platform
- Database
- Company
- Project
- Certification
- Degree
- Institution
- Job Title
- Responsibility
- Experience
- Location
- Date

---

## original_value

The value extracted directly from the source.

Example

```
Aws
```

---

## canonical_value

Normalized value.

Example

```
AWS
```

---

## normalized

Indicates whether normalization was applied.

```
true

false
```

---

# Source Object

```json
{
  "document_type": "",
  "section": "",
  "entry_index": 0,
  "page": 0,
  "line": 0,
  "character_offset": 0,
  "original_text": ""
}
```

---

## Source Fields

### document_type

Examples

- Resume
- Job Description

---

### section

Examples

- Skills
- Experience
- Projects
- Education
- Responsibilities
- Required Skills

---

### entry_index

Index of the parent record.

Example

```
Experience #2

↓

entry_index = 2
```

---

### page

Document page number.

Optional.

---

### line

Extracted line number.

Optional.

---

### character_offset

Character position inside the extracted text.

Optional.

---

### original_text

Complete sentence or phrase from which the entity originated.

Example

```
Designed ETL pipelines using Apache Spark on AWS.
```

---

# Confidence Object

```json
{
  "extraction": 0.0,
  "normalization": 0.0,
  "overall": 0.0
}
```

---

# Relationship Reference

Relationships are stored as references.

```json
[
  "REL-000001",
  "REL-000002"
]
```

Relationship definitions are stored separately.

---

# Metadata

```json
{
  "schema_version": "1.0",
  "created_by": "Entity Extraction Engine",
  "timestamp": ""
}
```

---

# Example

```json
{
  "entity_id": "ENT-000245",
  "entity_type": "Technology",
  "original_value": "Apache spark",
  "canonical_value": "Apache Spark",
  "normalized": true,
  "source": {
    "document_type": "Resume",
    "section": "Projects",
    "entry_index": 2,
    "page": 3,
    "line": 18,
    "character_offset": 642,
    "original_text": "Developed ETL pipelines using Apache Spark on AWS."
  },
  "confidence": {
    "extraction": 100,
    "normalization": 99,
    "overall": 99.5
  },
  "relationships": [
    "REL-000145",
    "REL-000146"
  ],
  "metadata": {
    "schema_version": "1.0",
    "created_by": "Entity Extraction Engine"
  }
}
```

---

# Validation Rules

Validate

- Duplicate Entity IDs
- Invalid Entity Types
- Missing Original Values
- Invalid Confidence Values
- Missing Source Information

Generate validation errors only.

---

# Schema Evolution

Rules

- Existing fields cannot be removed in minor versions.
- New fields must be optional until the next major version.
- Breaking changes require a new schema version.

---

# Ownership

Only the Entity Extraction module may create or modify Entity JSON.

Downstream engines consume the Entity JSON but must never mutate it.

---

# Dependencies

Consumes

- Resume JSON
- Job Description JSON

Produces

- Entity JSON

Consumed by

- Feature Engineering
- Hybrid Knowledge Layer
- Evidence Intelligence
- ATS Scoring

---

# Related Files

- Book_03_Entity_Extraction.md
- Resume_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Confidence.md
- Entity_Relationships.md

---

# End of Entity JSON Specification