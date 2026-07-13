# Feature Engineering Foundation Design Document

## Book 04 — Feature Engineering | Milestone 4.1

### Purpose

This document describes the architectural layout, implementation details, and design decisions for the Feature Engineering Foundation (Book 04). The milestone establishes a decoupled, stateless, and thread-safe dynamic framework for feature extraction from consolidated candidate entities.

---

### Key Architectural Decisions

#### 1. Decoupled Dynamic Registry and Factory
Instead of hardcoding concrete extractors, the system defines a case-insensitive `FeatureExtractorRegistry` that stores class references (`Type[FeatureExtractor]`). The `FeatureExtractorFactory` handles instantiation dynamically, ensuring clean separation of concerns and matching SOLID principles.

#### 2. Feature-Agnostic Orchestrator Pipeline
The pipeline (`FeatureEngineeringPipeline`) coordinates the execution of extractors sequentially without knowing their specific types or categories (e.g. skills, experience). It aggregates results and generates performance metrics.

#### 3. Deeply Generic Immutable Feature Schemas
The `Feature` model holds generic attributes (`feature_id`, `name`, `category`, `value`, `confidence`, `locations`, `provenance`, and `metadata`) and does not include ATS-specific fields (such as weights, scores, or compatibility ratings). Provenance origin details are explicitly captured in a generic `FeatureProvenance` schema.

---

### Component Overview

```
                        FeatureEngineeringService
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
FeatureExtractorRegistry   FeatureExtractorFactory   FeatureEngineeringPipeline
            │                       │                       │
     Class mappings            Creates objects          Sequencing & stats
```
