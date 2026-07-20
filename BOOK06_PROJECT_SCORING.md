# Book 06 — ATS Scoring Engine | Milestone 6.5

## 1. Overview
This specification details the design and execution architecture for **Milestone 6.5 — Project Scoring Engine**. The Project Scoring Engine executes deterministic raw score point calculations on Project matches. It determines the match classification (Exact, Similar project, Related project, Partial match, No Match) via `ProjectClassificationResolver`, accumulates weights, and returns a fully populated Project section score containing a generic, decoupled `ScoreBreakdown`.

---

## 2. Key Modules
* **ProjectScorer**: Coordinates validations, classification resolving, raw point accumulation, clamping, and generic `ScoreBreakdown` DTO construction. Inherits from `BaseSectionScorer`.
* **ProjectClassificationResolver**: Decouples the scorer from Book 05 metadata representations. Maps matching details into internal enums. Inherits from generic class `AbstractClassificationResolver[ProjectClassification]`.
* **ProjectScoreValidator**: Read-only validator verifying presence of project matches, absence of duplicates, and metadata validation constraints.
* **ProjectScoringRules**: Configurations defining weights for exact (3.0), similar project (2.5), related project (2.0), and partial match (1.0), clamping boundaries (max = 15.0), and related projects configs.
