# ATS Resume Intelligence Engine

# Job Description Entity Extraction

**Version:** 1.0

---

# Purpose

The Job Description Entity Extraction module converts the parsed Job Description JSON into standardized business entities.

Unlike the Job Description Parser, which preserves the original document structure, this module identifies and classifies hiring requirements that will later be used for Resume ↔ Job Description matching.

This module does not perform

- Resume Matching
- ATS Scoring
- Feature Engineering
- Semantic Analysis
- Requirement Prioritization

---

# Objectives

The module must

- Detect business entities.
- Classify extracted entities.
- Preserve original wording.
- Preserve source information.
- Assign extraction confidence.
- Produce deterministic Entity JSON.

---

# Inputs

Consumes

- Job Description JSON

Produced by

- JD Parser

---

# Outputs

Produces

- JD Entity JSON

Consumed by

- Feature Engineering

---

# Entity Extraction Pipeline

```
Job Description JSON

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

JD Entity JSON
```

---

# Sections Processed

The following sections are processed.

- Job Information
- Job Summary
- Responsibilities
- Required Skills
- Preferred Skills
- Experience Requirements
- Education Requirements
- Certifications
- Technical Stack
- Soft Skills
- Benefits
- Additional Information

---

# Supported Entity Types

## Job Information

Examples

- Job Title
- Department
- Employment Type
- Location
- Work Mode

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
- Kafka
- Docker

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

- Spring Boot
- .NET
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
- Google Cloud

---

## Tools

Examples

- Git
- Jenkins
- Terraform
- Airflow

---

## Responsibilities

Examples

- Build ETL pipelines
- Design REST APIs
- Lead engineering teams
- Develop microservices

---

## Experience Requirements

Examples

- 5+ years
- Data Engineering
- Cloud Experience

---

## Education

Examples

- Bachelor's Degree
- Master's Degree

---

## Certifications

Examples

- AWS Certified Solutions Architect
- Azure Administrator
- Databricks Data Engineer

---

## Industries

Examples

- Banking
- Healthcare
- Retail
- Manufacturing

---

## Domains

Examples

- Data Engineering
- Machine Learning
- Cyber Security
- DevOps

---

# Extraction Rules

## Rule 1

Extract only explicitly stated entities.

Never infer hidden requirements.

---

## Rule 2

Preserve original wording.

Do not rewrite.

---

## Rule 3

Preserve duplicate requirements.

Deduplication belongs to Entity Normalization.

---

## Rule 4

Preserve source section.

Example

```
Required Skills

↓

Python
```

---

## Rule 5

Preserve source text.

Every entity must maintain a reference to its original location.

---

# Source Mapping

Each entity records

- Section
- Original Text
- Entity Type

Example

```
Responsibilities

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
| AWS | 100% |
| Apache Spark | 99% |
| Postgre SQL | 91% |

Confidence measures extraction quality only.

It never affects ATS scoring.

---

# Validation

Validate

- Empty entities
- Invalid sections
- Corrupted values
- Missing required fields

Return warnings only.

---

# Error Handling

Possible Errors

- Invalid JD JSON
- Unsupported Section
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

- Job Description JSON

Produces

- JD Entity JSON

Consumed by

- Feature Engineering

---

# Related Files

- Book_03_Entity_Extraction.md
- Resume_Entity_Extraction.md
- Entity_Normalization.md
- Entity_Confidence.md
- Entity_Relationships.md
- Entity_JSON_Specification.md

---

# End of Job Description Entity Extraction