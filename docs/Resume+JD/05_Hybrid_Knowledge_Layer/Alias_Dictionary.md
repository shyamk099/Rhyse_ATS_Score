# ATS Resume Intelligence Engine

# Alias Dictionary

**Version:** 1.0

---

# Purpose

The Alias Dictionary defines the canonical alias mappings used by the Alias Matching Engine.

It provides a deterministic mapping between commonly used names, abbreviations, acronyms, and their canonical business representation.

The Alias Dictionary is a version-controlled knowledge asset.

---

# Objectives

The Alias Dictionary must

- Maintain canonical mappings.
- Resolve official aliases.
- Resolve abbreviations.
- Support deterministic matching.
- Remain version controlled.

---

# Scope

The Alias Dictionary covers

- Technologies
- Programming Languages
- Frameworks
- Cloud Platforms
- Databases
- DevOps Tools
- Certifications
- Job Titles

This dictionary does not contain

- Technology Relationships
- Semantic Similarity
- Typographical Corrections

---

# Dictionary Architecture

```
Alias

↓

Canonical Value

↓

Entity Type

↓

Dictionary
```

---

# Dictionary Philosophy

Every alias represents exactly one canonical value.

Every canonical value may have multiple aliases.

Example

```
AWS

↓

Amazon Web Services
```

```
Amazon Web Services

↓

AWS
```

Both resolve to the same canonical entity.

---

# Dictionary Structure

Each dictionary entry contains

- Alias ID
- Alias
- Canonical Value
- Entity Type
- Status
- Version

---

# Example Entries

## Programming Language

```
Alias

JS

↓

Canonical

JavaScript
```

---

## Framework

```
Alias

Dot Net

↓

Canonical

.NET
```

---

## Cloud Platform

```
Alias

Amazon Web Services

↓

Canonical

AWS
```

---

## Database

```
Alias

MS SQL

↓

Canonical

Microsoft SQL Server
```

---

## Certification

```
Alias

AWS SAA

↓

Canonical

AWS Certified Solutions Architect – Associate
```

---

## Job Title

```
Alias

SDE

↓

Canonical

Software Development Engineer
```

---

# Dictionary Entry

Example

```json
{
    "alias_id": "ALIAS-000145",
    "alias": "AWS SAA",
    "canonical_value": "AWS Certified Solutions Architect – Associate",
    "entity_type": "Certification",
    "status": "Active",
    "version": "1.0"
}
```

---

# Dictionary Rules

## Rule 1

Every alias maps to exactly one canonical value.

---

## Rule 2

Canonical values are unique.

---

## Rule 3

Aliases are case-insensitive.

---

## Rule 4

Aliases never reference ontology relationships.

---

## Rule 5

Aliases never perform semantic reasoning.

---

## Rule 6

Aliases are manually curated and version controlled.

---

# Validation

Validate

- Duplicate Aliases
- Multiple Canonical Values
- Invalid Entity Types
- Empty Aliases
- Missing Canonical Values

Return validation failures only.

---

# Versioning

Each release includes

- Dictionary Version
- Entry Count
- Release Date

Dictionary updates are independent of Algorithm updates.

---

# Ownership

The Alias Dictionary is maintained independently from the matching engine.

The Alias Matching Engine consumes the dictionary.

It never modifies it.

---

# Dependencies

Consumes

- Canonical Entity Names

Produces

- Alias Knowledge Base

Consumed by

- Alias Matching Engine

---

# Related Files

- Book_05_Hybrid_Knowledge_Layer.md
- Alias_Matching.md
- Technology_Ontology.md
- Matching_Pipeline.md
- Matching_Confidence.md
- Match_JSON_Specification.md

---

# End of Alias Dictionary