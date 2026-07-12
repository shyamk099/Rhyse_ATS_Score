# ATS Resume Intelligence Engine

# Canonical JSON Schemas

**Version:** 1.0

---

# Purpose

This document defines the canonical JSON structures used throughout the ATS Resume Intelligence Engine.

These schemas serve as the contract between all engines.

Every engine consumes and produces structured JSON based on these schemas.

No engine should modify the schema without updating this document.

---

# Design Principles

The canonical schemas follow these principles.

- Immutable Input
- Deterministic Structure
- Version Controlled
- Engine Independent
- Extensible
- Backward Compatible

---

# Processing Flow

```
Resume

↓

Resume JSON

↓

Entity JSON

↓

Feature JSON

↓

Evidence JSON

↓

Score JSON

↓

API Response
```

---

# Canonical Objects

The system defines six canonical objects.

| Object | Produced By | Consumed By |
|----------|-------------|-------------|
| Resume JSON | Resume Parser | Entity Extraction |
| Job Description JSON | JD Parser | Entity Extraction |
| Entity JSON | Entity Extraction | Feature Engineering |
| Feature JSON | Feature Engineering | Matching Engine |
| Evidence JSON | Evidence Intelligence | Matching & Output |
| Score JSON | Scoring Engine | Output API |

---

# Resume JSON

```json
{
  "metadata": {},
  "contact": {},
  "summary": "",
  "skills": [],
  "experience": [],
  "projects": [],
  "education": [],
  "certifications": [],
  "awards": [],
  "languages": [],
  "raw_text": "",
  "validation": {},
  "parser_confidence": 0.0
}
```

---

# Job Description JSON

```json
{
  "metadata": {},
  "job_information": {},
  "summary": "",
  "responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "experience_requirements": [],
  "education_requirements": [],
  "certifications": [],
  "technical_stack": [],
  "soft_skills": [],
  "raw_text": "",
  "validation": {},
  "parser_confidence": 0.0
}
```

---

# Entity JSON

Produced by Book 03.

```json
{
  "skills": [],
  "companies": [],
  "projects": [],
  "technologies": [],
  "degrees": [],
  "certifications": [],
  "locations": [],
  "dates": [],
  "titles": []
}
```

---

# Feature JSON

Produced by Book 04.

```json
{
  "years_of_experience": 0,
  "career_progression": {},
  "skill_density": {},
  "leadership": {},
  "resume_statistics": {},
  "section_completeness": {},
  "project_statistics": {}
}
```

---

# Evidence JSON

Produced by Book 06.

```json
{
  "requirement_id": "",
  "match_type": "",
  "confidence": 0.0,
  "sources": [],
  "explanation": ""
}
```

---

# Score JSON

Produced by Book 07.

```json
{
  "ats_compatibility": 0,
  "resume_quality": 0,
  "resume_jd_match": 0,
  "integrity_penalty": 0,
  "overall_score": 0
}
```

---

# API Response

Produced by Book 09.

```json
{
  "score": {},
  "confidence": {},
  "matched_requirements": [],
  "missing_requirements": [],
  "evidence": [],
  "warnings": [],
  "version": {}
}
```

---

# Object Ownership

| Object | Owner |
|----------|-------|
| Resume JSON | Resume Parser |
| JD JSON | JD Parser |
| Entity JSON | Entity Extraction |
| Feature JSON | Feature Engineering |
| Evidence JSON | Evidence Intelligence |
| Score JSON | ATS Scoring |
| API Response | Output Engine |

Only the owning engine may create or modify its object.

Downstream engines consume objects but do not mutate them.

---

# Versioning

Every canonical object must include schema version metadata.

Example

```json
{
  "schema_version": "1.0"
}
```

This allows backward compatibility when schemas evolve.

---

# Schema Evolution Rules

Rules

- Never remove existing fields in a minor version.
- New fields must be optional until the next major version.
- Breaking changes require a major version increment.
- Schema changes must update this document before implementation.

---

# Dependencies

Book 03 consumes

- Resume JSON
- JD JSON

Book 04 consumes

- Entity JSON

Book 05 consumes

- Feature JSON

Book 06 produces

- Evidence JSON

Book 07 produces

- Score JSON

Book 09 produces

- API Response

---

# End of Canonical JSON Schemas