# Book 06 — ATS Scoring Engine | Milestone 6.4

## 1. Overview
This specification details the design and execution architecture for **Milestone 6.4 — Education Scoring Engine**. The Education Scoring Engine executes deterministic raw score point calculations on Education matches. It determines the match classification (Exact, Higher than required, Related field, Lower than required, Unrelated field, No Match) via `EducationClassificationResolver`, accumulates weights, and returns a fully populated Education section score containing a generic, decoupled `ScoreBreakdown`.

---

## 2. Key Modules
* **EducationScorer**: Coordinates validations, classification resolving, raw point accumulation, clamping, and generic `ScoreBreakdown` DTO construction. Inherits from `BaseSectionScorer`.
* **EducationClassificationResolver**: Decouples the scorer from Book 05 metadata representations. Maps matching details into internal enums. Inherits from generic class `AbstractClassificationResolver[EducationClassification]`.
* **EducationScoreValidator**: Read-only validator verifying presence of education matches, absence of duplicates, and metadata validation constraints.
* **EducationScoringRules**: Configurations defining weights for exact (4.0), higher (4.0), related (2.5), lower (1.0), and unrelated (0.0) matches, clamping boundaries (max = 15.0), and related fields configs.
