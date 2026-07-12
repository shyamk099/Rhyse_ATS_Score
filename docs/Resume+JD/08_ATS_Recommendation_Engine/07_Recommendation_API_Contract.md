# ATS Resume Intelligence Engine

# Recommendation API Contract

**Version:** 1.0

---

# Purpose

The Recommendation API exposes the ATS Recommendation Engine to external consumers.

It provides a stable, versioned API for retrieving structured Resume improvement recommendations.

The Recommendation API never performs Resume rewriting.

It only analyzes, validates, and publishes Recommendation JSON.

---

# Objectives

The Recommendation API must

- Accept Resume and Job Description.
- Generate ATS recommendations.
- Return Recommendation JSON.
- Preserve version compatibility.
- Support external integrations.

---

# Scope

This module covers

- REST API
- Request Validation
- Response Contract
- Error Handling
- API Versioning

This module does not cover

- Resume Rewriting
- Prompt Engineering
- ATS Scoring Logic
- Resume Matching Logic

---

# Architecture

```
Client

↓

Recommendation API

↓

ATS Recommendation Engine

↓

Recommendation JSON

↓

Response
```

---

# API Version

```
/api/v1
```

Future breaking changes require a new version.

Example

```
/api/v2
```

---

# Endpoint 1

## Generate Recommendations

### Endpoint

```http
POST /api/v1/recommendations
```

---

### Description

Analyzes a Resume against a Job Description and returns structured recommendations.

---

### Request

```json
{
    "resume_id": "RES-001",

    "job_description_id": "JD-001",

    "resume": "...",

    "job_description": "..."
}
```

---

### Response

```json
{
    "evaluation_id": "EVAL-001",

    "current_score": 74,

    "recommendation_count": 8,

    "recommendations": [

    ]
}
```

---

# Endpoint 2

## Get Recommendation Report

### Endpoint

```http
GET /api/v1/recommendations/{evaluation_id}
```

---

### Description

Returns the Recommendation JSON previously generated for an evaluation.

---

### Response

Returns

Recommendation JSON.

---

# Endpoint 3

## Get API Version

### Endpoint

```http
GET /api/v1/version
```

---

### Response

```json
{
    "api_version": "1.0",

    "algorithm_version": "3.2",

    "recommendation_engine": "1.0"
}
```

---

# Endpoint 4

## Health Check

### Endpoint

```http
GET /api/v1/health
```

---

### Response

```json
{
    "status": "Healthy",

    "service": "ATS Recommendation Engine",

    "version": "1.0"
}
```

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Evaluation Not Found |
| 409 | Duplicate Evaluation |
| 422 | Validation Failed |
| 429 | Rate Limited |
| 500 | Internal Error |

---

# Request Validation

Validate

- Resume Exists
- Job Description Exists
- Required Fields
- Supported File Type
- Request Size
- Encoding

Invalid requests are rejected before analysis.

---

# Authentication

Supported mechanisms

- API Key
- OAuth2
- JWT

Authentication strategy is configurable.

---

# Response Principles

Every response must be

- Deterministic
- Versioned
- Traceable
- Explainable

---

# Error Response

Example

```json
{
    "error": {

        "code": "REQ-401",

        "message": "Missing Job Description.",

        "details": "job_description is required.",

        "timestamp": "2026-07-12T16:30:00Z"
    }
}
```

---

# Rate Limiting

The API may apply configurable limits.

Example

```
100 requests

per minute

per API key
```

Rate limits are configurable.

---

# Security Rules

- All endpoints require HTTPS.
- Authentication is required except Health Check.
- Sensitive data must never be logged.
- Request payloads must be validated.
- Recommendation JSON must remain immutable after publication.

---

# Dependencies

Consumes

- Resume
- Job Description

Produces

- Recommendation JSON

Consumed by

- Resume Intelligence Repository
- Dashboard
- Output API
- Analytics Engine
- Third-party Integrations

---

# Related Files

- Book_08_ATS_Recommendation_Engine.md
- 01_Gap_Analysis.md
- 02_Recommendation_Generation.md
- 03_Recommendation_Prioritization.md
- 04_Score_Impact_Estimation.md
- 05_Recommendation_Validation.md
- 06_Recommendation_JSON_Specification.md

---

# End of Recommendation API Contract