# ATS Resume Intelligence Engine

# Score Versioning

**Version:** 1.0

---

# Purpose

The Score Versioning Engine records the complete version history of every ATS evaluation.

Its responsibility is to ensure that every ATS Score is reproducible, traceable, and comparable across product releases.

Score Versioning never changes scores.

It only records the versions of every algorithm that contributed to the evaluation.

---

# Objectives

The Score Versioning Engine must

- Track algorithm versions.
- Track scoring versions.
- Track ontology versions.
- Track embedding model versions.
- Track calibration versions.
- Guarantee reproducibility.

---

# Scope

This module covers

- Algorithm Version
- Weight Version
- Calibration Version
- Ontology Version
- Alias Dictionary Version
- Embedding Model Version
- Parser Version
- Pipeline Version

This module does not cover

- ATS Scoring
- Resume Matching
- Resume Parsing
- Resume Optimization

---

# Inputs

Consumes

- Final ATS Score
- Evaluation Metadata

Produced by

- ATS Scoring Engine
- Pipeline Configuration

---

# Outputs

Produces

- Version Metadata

Consumed by

- Score JSON
- Analytics Engine
- Audit Engine
- Output API

---

# Design Philosophy

The Score Versioning Engine answers one question.

> "Exactly which versions of every engine produced this ATS Score?"

Every ATS evaluation must be reproducible years later.

---

# Processing Pipeline

```
Pipeline Configuration

↓

Version Collection

↓

Version Validation

↓

Version Metadata

↓

Score JSON
```

---

# Version Components

Each ATS evaluation records

## Algorithm Version

Version of the overall ATS algorithm.

Example

```
3.2.0
```

---

## Weight Version

Version of the scoring weights.

Example

```
2.1
```

---

## Calibration Version

Version of the calibration rules.

Example

```
1.4
```

---

## Ontology Version

Version of the technology ontology.

Example

```
5.3
```

---

## Alias Dictionary Version

Version of the alias mappings.

Example

```
4.8
```

---

## Embedding Model Version

Version of the semantic model.

Examples

- BGE-v1.5
- E5-Large-v2
- OpenAI-Embedding-3-Large

---

## Parser Version

Version of the Resume Parser.

---

## Pipeline Version

Version of the complete ATS pipeline.

---

# Example

```
ATS Evaluation

↓

Algorithm

3.2.0

↓

Weights

2.1

↓

Ontology

5.3

↓

Embedding

BGE-v1.5

↓

Calibration

1.4

↓

Pipeline

3.2
```

---

# Version Rules

## Rule 1

Every ATS evaluation records every version.

---

## Rule 2

Versions are immutable.

---

## Rule 3

Versions never change after evaluation.

---

## Rule 4

Changing any engine version creates a new evaluation version.

---

## Rule 5

Historical evaluations are never modified.

---

# Validation

Validate

- Missing Algorithm Version
- Missing Weight Version
- Missing Calibration Version
- Missing Ontology Version
- Missing Embedding Version
- Missing Pipeline Version

Return validation failures only.

---

# Version Metadata

```json
{
    "algorithm_version": "",
    "weight_version": "",
    "calibration_version": "",
    "ontology_version": "",
    "alias_dictionary_version": "",
    "embedding_model_version": "",
    "parser_version": "",
    "pipeline_version": "",
    "generated_at": ""
}
```

---

# Example

```json
{
    "algorithm_version": "3.2.0",
    "weight_version": "2.1",
    "calibration_version": "1.4",
    "ontology_version": "5.3",
    "alias_dictionary_version": "4.8",
    "embedding_model_version": "BGE-v1.5",
    "parser_version": "2.0",
    "pipeline_version": "3.2",
    "generated_at": "2026-07-12T14:20:00Z"
}
```

---

# Non-Functional Requirements

The Versioning Engine must be

- Deterministic
- Immutable
- Auditable
- Traceable
- Backward Compatible

---

# Dependencies

Consumes

- Final ATS Score
- Pipeline Configuration

Produces

- Version Metadata

Consumed by

- Score_JSON_Specification.md
- ATS_Final_Score.md
- Output API
- Analytics Engine

---

# Related Files

- Book_07_ATS_Scoring.md
- Weighted_Scoring_Engine.md
- Score_Calibration.md
- Score_JSON_Specification.md
- ATS_Final_Score.md

---

# End of Score Versioning