# ATS Resume Intelligence Engine - Handbook-Ordered Implementation Plan

## Implementation constraint

This is a sequencing plan only. It does not authorize implementation or introduce business rules. “Classes” below means logical implementation boundaries required by the handbook; concrete names, language, and framework remain unselected.

## Phase 1 - Approved foundation sequence

Phase 1 is an implementation-sequencing prerequisite. It establishes no parser, entity, feature, matching, evidence, scoring, or recommendation business rules. Book 09 remains the implementation authority for rule behavior; only the technical foundation for loading and serving future approved rules is created here.

### Milestone 1.1 - Project Structure

**Purpose:** establish the approved Clean Architecture module boundaries and dependency direction. **Files:** project/package layout only. **Classes/interfaces:** composition-root boundary and package markers only. **Dependencies:** none. **Acceptance criteria:** business-domain modules have no infrastructure dependency. **Testing scope:** import/dependency-direction checks. **Deliverables:** approved empty project structure.

### Milestone 1.2 - Configuration

**Purpose:** establish infrastructure configuration loading distinct from frozen business rules. **Files:** configuration boundary only. **Classes/interfaces:** configuration provider and typed infrastructure-settings contract. **Dependencies:** M1.1. **Acceptance criteria:** no business-rule values are hardcoded or introduced. **Testing scope:** valid/invalid infrastructure configuration loading. **Deliverables:** configuration boundary.

### Milestone 1.3 - Logging

**Purpose:** establish safe, structured observability for future stages. **Files:** logging boundary only. **Classes/interfaces:** logger provider and correlation-context contract. **Dependencies:** M1.1-M1.2. **Acceptance criteria:** logging contains no sensitive document payloads and does not influence business outcomes. **Testing scope:** redaction and correlation tests. **Deliverables:** logging boundary.

### Milestone 1.4 - Rule Engine Foundation

**Purpose:** establish Rule Loader, Rule Validator, Rule Registry, Runtime Rule Provider, Rule Models, Rule Cache, and dependency-injection wiring without implementing any business-rule content. **Files:** `09_ATS_Rule_Engine/*` as architecture reference; rule-engine foundation package. **Classes/interfaces:** Rule Loader, Rule Validator, Rule Registry, Runtime Rule Provider, Rule Models, Rule Cache, DI wiring. **Dependencies:** M1.1-M1.3 and authoritative Rule JSON schema. **Acceptance criteria:** only structurally valid, immutable rule documents can be loaded, registered, cached, and provided at runtime; no parser/entity/feature/matching/evidence/scoring/recommendation rule semantics are implemented. **Testing scope:** structural validation, registry/cache behavior, immutability, dependency injection. **Deliverables:** Rule Engine technical foundation.

### Milestone 01 - System Architecture

**Purpose:** compose the five layers and adjacent-layer-only dependency direction.

**Files:** `01_System_Architecture/*`; composition root, cross-cutting validation/error/observability interfaces. **Classes/interfaces:** engine ports, output port, rule provider, dependency-composition boundary. **Dependencies:** Phase 1. **Acceptance criteria:** all engine ownership and data flows match Book 01. **Testing scope:** dependency/contract integration tests. **Deliverables:** approved component and sequence diagrams.

### Milestone 02 - Document Processing

**Purpose:** validate, extract, parse, and validate Resume/JD documents into canonical JSON with confidence.

**Files:** `02_Document_Processing/*`; document-processing package and canonical Resume/JD contracts. **Classes/interfaces:** upload validator, type detector, OCR detector/processor, text extractor, Resume parser, JD parser, schema validator. **Dependencies:** M01; Rule Engine Foundation; approved parser-rule content; authoritative supported-format/OCR decisions. **Acceptance criteria:** required Resume/JD fields, source text, validation, and parser confidence conform to the canonical schema. **Testing scope:** supported/invalid formats, OCR/no-OCR, extraction order, malformed content, schema validation. **Deliverables:** immutable Resume JSON and JD JSON.

### Milestone 03 - Entity Extraction

**Purpose:** extract source-traceable entities, normalize without losing original values, form relationships, and calculate confidence.

**Files:** `03_Entity_Extraction/*`; entity-extraction package and Entity JSON contract. **Classes/interfaces:** Resume/JD extractor, normalizer, relationship builder, entity-confidence calculator. **Dependencies:** M02; Rule Engine Foundation; approved entity-rule content; alias/ontology assets. **Acceptance criteria:** entity provenance, canonical/original values, relationships, and confidence satisfy the Entity JSON specification. **Testing scope:** each supported entity type, normalization preservation, relationship validation, confidence boundaries. **Deliverables:** immutable Entity JSON.

### Milestone 04 - Feature Engineering

**Purpose:** calculate primitive and derived Resume/JD features without matching or scoring.

**Files:** `04_Feature_Engineering/*`; feature-engineering package and Feature JSON contract. **Classes/interfaces:** Resume/JD feature calculator, derived-feature calculator, confidence calculator, feature validator. **Dependencies:** M03; Rule Engine Foundation; approved feature-rule content. **Acceptance criteria:** all feature values retain entity traceability and no feature module performs matching/scoring. **Testing scope:** calculations, dependency rules, confidence, missing source entities. **Deliverables:** immutable Resume and JD Feature JSON.

### Milestone 05 - Hybrid Knowledge Layer

**Purpose:** compare feature pairs using the approved fixed matching order and emit immutable Match JSON.

**Files:** `05_Hybrid_Knowledge_Layer/*`; knowledge-matching package, alias dictionary/ontology/model adapters. **Classes/interfaces:** matching orchestrator; exact, alias, fuzzy, ontology, semantic strategies; match-confidence calculator; Match JSON validator. **Dependencies:** M04; Rule Engine Foundation; approved matching-rule content; alias dictionary, ontology, embedding adapter/version. **Acceptance criteria:** only one strategy is recorded per match; match reasons, confidence, relevant versions, and provenance are complete. **Testing scope:** strategy precedence, threshold edges, non-matches, ontology traversal, semantic adapter determinism. **Deliverables:** immutable Match JSON.

### Milestone 06 - Evidence Intelligence

**Purpose:** generate evidence once, validate it, calculate requirement/section coverage and confidence, aggregate and explain it.

**Files:** `06_Evidence_Intelligence/*`; evidence-intelligence package and Evidence JSON contract. **Classes/interfaces:** evidence generator, requirement/section evidence builders, validator, confidence calculator, aggregator, explanation builder. **Dependencies:** M05; Rule Engine Foundation; approved evidence-rule content. **Acceptance criteria:** each evaluation has one Evidence JSON; requirements, sections, references, coverage, confidence, and explanations validate; downstream consumers do not mutate it. **Testing scope:** evidence generation, missing/broken references, coverage/calculation boundaries, explanation traceability. **Deliverables:** immutable Evidence JSON.

### Milestone 07 - ATS Scoring

**Purpose:** independently calculate components, apply immutable weights and integrity penalty once, calibrate and publish Score JSON.

**Files:** `07_ATS_Scoring/*`; ATS-scoring package and Score JSON contract. **Classes/interfaces:** compatibility, quality, JD-match, semantic-validation, integrity calculators; weighted scorer; calibrator; version manager; score publisher/validator. **Dependencies:** M06; Rule Engine Foundation; approved scoring-rule content; calibration data/specification. **Acceptance criteria:** only scoring calculates score; evidence is not changed; positive weights total 100%; penalty is unweighted/once; final score is bounded; confidence never alters score. **Testing scope:** formula, weights, penalty cap/boundaries, calibration, version reproducibility, score schema. **Deliverables:** immutable Score JSON and published evaluation.

### Milestone 08 - ATS Recommendation Engine

**Purpose:** transform evidence and scores into truthful, validated, prioritized recommendations without rewriting a resume.

**Files:** `08_ATS_Recommendation_Engine/*`; recommendation package, Recommendation JSON, API adapter. **Classes/interfaces:** gap analyzer, recommendation generator, impact estimator, prioritizer, validator, report repository, API controller/response mapper. **Dependencies:** M06-M07; Rule Engine Foundation; approved recommendation-rule content; persistent report store; auth/rate-limit infrastructure. **Acceptance criteria:** every recommendation is evidence-backed, deterministic, independently validated, prioritized, versioned, and never claims a score change as fact. **Testing scope:** gaps, prioritization, impact ranges/confidence, ethics/reference validation, documented endpoints/status/error contracts. **Deliverables:** Recommendation JSON and `/api/v1` contract implementation.

### Milestone 09 - ATS Rule Engine

**Purpose:** complete Book 09 rule behavior incrementally after each consuming handbook phase is approved, without changing the Phase 1 foundation.

**Files:** `09_ATS_Rule_Engine/*`; external approved rule configuration assets. **Classes/interfaces:** category-specific rule validators/providers that extend the Phase 1 foundation. **Dependencies:** Rule Engine Foundation; approved rule content; corresponding consuming contracts. **Acceptance criteria:** each activated rule category is validated, versioned, immutable, and traceable; runtime engines never modify active rules. **Testing scope:** category rule validation, version compatibility, activation/audit, and consumer integration. **Deliverables:** approved, activated rule categories aligned with Books 02-08.

## OPEN QUESTIONS

Implementation must stop before Milestone 02 until the open questions in `ARCHITECTURE.md` are resolved, particularly missing rule/configuration assets, matching-order conflict, and undefined score/calibration/penalty semantics.
