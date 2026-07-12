# ATS Resume Intelligence Engine

# Resume Entity Extraction

**Version:** 1.0

---

# Purpose

The Resume Entity Extraction module converts the parsed Resume JSON into standardized business entities.

Unlike the Resume Parser, which preserves the original document structure, this module identifies and classifies meaningful entities that will be used by downstream intelligence engines.

This module does not perform

- ATS Scoring
- Feature Engineering
- Resume Matching
- Semantic Analysis
- Evidence Generation

---

# Objectives

The module must

- Detect resume entities.
- Classify extracted entities.
- Preserve original values.
- Preserve source location.
- Assign extraction confidence.
- Produce deterministic Entity JSON.

---

# Inputs

Consumes

- Resume JSON

Produced by

- Resume Parser

---

# Outputs

Produces

- Resume Entity JSON

Consumed by

- Feature Engineering

---

# Entity Extraction Pipeline

```
Resume JSON

↓

Section Selection

↓

Entity Detection

↓

Entity Classification

↓

Normalization

↓

Confidence Assignment

↓

Resume Entity JSON
```

---

# Resume Sections Processed

The following sections are scanned.

- Contact
- Summary
- Skills
- Experience
- Projects
- Education
- Certifications
- Awards
- Languages

---

# Supported Entity Types

## Contact

Examples

- Name
- Email
- Phone
- LinkedIn
- GitHub
- Portfolio

---

## Skills

Examples

- Python
- SQL
- AWS
- Kubernetes

---

## Technologies

Examples

- Apache Spark
- Databricks
- Docker
- Kafka

---

## Programming Languages

Examples

- Python
- Java
- C#
- Go

---

## Frameworks

Examples

- .NET
- Spring Boot
- Django
- React

---

## Databases

Examples

- PostgreSQL
- MongoDB
- SQL Server
- Oracle

---

## Cloud Platforms

Examples

- AWS
- Azure
- GCP

---

## Tools

Examples

- Git
- Jenkins
- Terraform
- Docker

---

## Companies

Examples

- Microsoft
- Amazon
- Infosys

---

## Job Titles

Examples

- Data Engineer
- Software Engineer
- DevOps Engineer

---

## Projects

Examples

Project Name

Project Description

Responsibilities

Technologies

---

## Education

Examples

Degree

Institution

Graduation Year

---

## Certifications

Examples

AWS Certified Solutions Architect

Databricks Data Engineer

Azure Administrator

---

## Locations

Examples

Chennai

London

New York

---

## Dates

Examples

Employment Dates

Graduation Dates

Certification Dates

---

# Extraction Rules

## Rule 1

Extract only explicit entities.

Never infer.

---

## Rule 2

Preserve original values.

Example

```
Apache Spark

↓

Apache Spark
```

Never rewrite.

---

## Rule 3

Preserve duplicate entities.

Deduplication belongs to Entity Normalization.

---

## Rule 4

Preserve source section.

Example

```
AWS

↓

Skills Section
```

---

## Rule 5

Preserve source text.

Every entity must maintain a reference to its originating text.

---

# Source Mapping

Every entity records

- Section
- Original Text
- Entity Type

Example

```
Experience

↓

Apache Spark

↓

Technology
```

---

# Confidence

Each extracted entity receives an extraction confidence.

Example

| Entity | Confidence |
|---------|-----------:|
| Python | 100% |
| Apache Spark | 100% |
| Postgre SQL | 91% |
| Aws | 88% |

Confidence measures extraction quality only.

It never affects ATS scoring.

---

# Validation

Validate

- Empty entities
- Corrupted values
- Invalid dates
- Missing required fields

Return warnings only.

---

# Error Handling

Possible Errors

- Unsupported Resume JSON
- Invalid Section
- Corrupted Entity
- Missing Metadata

Each error returns

- Error Code
- Error Message
- Suggested Resolution

---

# Non-Functional Requirements

The module must be

- Deterministic
- Stateless
- Repeatable
- Explainable
- Extensible

---

# Dependencies

Consumes

- Resume JSON

Produces

- Resume Entity JSON

Consumed by

- Feature Engineering

---

# Related Files

- Book_03_Entity_Extraction.md
- JD_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Confidence.md
- Entity_Relationships.md
- Entity_JSON_Specification.md

---

# End of Resume Entity Extraction