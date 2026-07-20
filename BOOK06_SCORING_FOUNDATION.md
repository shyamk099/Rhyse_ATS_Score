# Book 06 — ATS Scoring Engine | Milestone 6.1

## 1. Overview
This specification details the design and execution architecture for **Milestone 6.1 — Scoring Foundation**. The Scoring Foundation is responsible for consolidating individual match results into a structured, immutable scoring evaluation contract. It processes `CanonicalMatchCollection` objects and compiles a structured `ScoreResult` container populated with telemetry, metadata, and placeholder scores.

---

## 2. Key Modules
* **ScoringService**: Facade exposing the public coordination entry points.
* **ScoringPipeline**: Manages E2E validation, registry querying, prioritization sorting, and DTO compilation.
* **ScoringRegistry**: Thread-safe registry mapping names to abstract scorer implementations.
* **ScoringFactory**: Dependency-injection constructors.
* **ScoreValidator**: Read-only validator checking rule versions, match collection integrity, and category constraints.
* **ScoringRules**: Governing configuration payload versioned and strictness controlled.
