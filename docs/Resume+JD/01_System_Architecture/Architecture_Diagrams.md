# ATS Resume Intelligence Engine

# Architecture Diagrams

**Version:** 1.0

---

# Purpose

This document contains the architectural diagrams for the ATS Resume Intelligence Engine.

Unlike Book_01_System_Architecture.md, which defines the architecture conceptually, this document provides visual representations of the system.

These diagrams are intended for architects, developers, QA engineers, and product teams.

---

# Diagram 1 — Layered Architecture

```text
                    ATS Resume Intelligence Engine

┌────────────────────────────────────────────────────────────┐
│                  Presentation Layer                        │
│------------------------------------------------------------│
│ Resume Upload │ JD Upload │ REST API │ Authentication      │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   Processing Layer                         │
│------------------------------------------------------------│
│ Document Parser                                            │
│ Entity Extraction                                          │
│ Feature Engineering                                        │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                  Intelligence Layer                        │
│------------------------------------------------------------│
│ Hybrid Knowledge Layer                                     │
│ Evidence Intelligence Engine                               │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    Scoring Layer                           │
│------------------------------------------------------------│
│ ATS Compatibility                                           │
│ Resume Quality                                              │
│ Resume ↔ JD Matching                                        │
│ Integrity Engine                                            │
│ Weighted Score Engine                                       │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                     Output Layer                           │
│------------------------------------------------------------│
│ Confidence Aggregator                                      │
│ Output Engine                                               │
└────────────────────────────────────────────────────────────┘
```

---

# Diagram 2 — End-to-End Processing Pipeline

```text
Resume                     Job Description
      │                           │
      ▼                           ▼

Document Ingestion

↓

Document Parser

↓

Entity Extraction

↓

Feature Engineering

↓

Hybrid Knowledge Layer

↓

Evidence Intelligence Engine

↓

ATS Compatibility Engine

↓

Resume Quality Engine

↓

Resume ↔ JD Matching Engine

↓

Integrity Engine

↓

Weighted Score Engine

↓

Confidence Aggregator

↓

Output Engine

↓

JSON Response
```

---

# Diagram 3 — Resume Processing Flow

```text
Resume

↓

Parser

↓

Resume JSON

↓

Entity Extraction

↓

Resume Entities

↓

Feature Engineering

↓

Resume Features
```

---

# Diagram 4 — Job Description Processing Flow

```text
Job Description

↓

Parser

↓

JD JSON

↓

Entity Extraction

↓

JD Entities

↓

Feature Engineering

↓

JD Features
```

---

# Diagram 5 — Matching Pipeline

```text
Resume Features

+

JD Features

↓

Exact Match

↓

Alias Match

↓

Fuzzy Match

↓

Ontology Match

↓

Semantic Match

↓

Evidence Object

↓

Requirement Confidence
```

---

# Diagram 6 — Scoring Pipeline

```text
ATS Compatibility Score

+

Resume Quality Score

+

Resume ↔ JD Match Score

↓

Raw Score

↓

Integrity Penalty

↓

Clamp (0–100)

↓

Final ATS Score
```

---

# Diagram 7 — Evidence Flow

```text
Resume

↓

Skill

↓

Experience

↓

Project

↓

Certification

↓

Evidence Validation

↓

Evidence Object

↓

Requirement Confidence
```

---

# Diagram 8 — Shared Components

```text
                Resume Only

                       │

                       ▼

          Resume Quality Engine

                       ▲

                       │

                Resume + JD
```

---

# Diagram 9 — Confidence Flow

```text
Parser Confidence

+

Extraction Confidence

+

Evidence Confidence

+

Matching Confidence

↓

Confidence Aggregator

↓

Overall Confidence

Section Confidence

Requirement Confidence
```

---

# Diagram 10 — Output Model

```text
ATS Score

↓

Section Scores

↓

Matched Requirements

↓

Missing Requirements

↓

Evidence

↓

Confidence

↓

Version Metadata

↓

API Response
```

---

# Diagram Relationships

| Diagram | Description |
|----------|-------------|
| Diagram 1 | Layered Architecture |
| Diagram 2 | Complete Processing Flow |
| Diagram 3 | Resume Pipeline |
| Diagram 4 | Job Description Pipeline |
| Diagram 5 | Matching Process |
| Diagram 6 | Score Calculation |
| Diagram 7 | Evidence Generation |
| Diagram 8 | Shared Components |
| Diagram 9 | Confidence Aggregation |
| Diagram 10 | Output Flow |

---

# End of Architecture Diagrams