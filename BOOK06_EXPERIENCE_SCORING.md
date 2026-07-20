# Book 06 — ATS Scoring Engine | Milestone 6.3

## 1. Overview
This specification details the design and execution architecture for **Milestone 6.3 — Experience Scoring Engine**. The Experience Scoring Engine executes deterministic raw score point calculations on Experience matches. It determines the match classification (Exact, Partial, Overqualified, Underqualified, No Match) via `ExperienceClassificationResolver`, accumulates weights, and returns a fully populated Experience section score containing a generic, decoupled `ScoreBreakdown`.

---

## 2. Key Modules
* **ExperienceScorer**: Coordinates validations, classification resolving, raw point accumulation, clamping, and generic `ScoreBreakdown` DTO construction. Inherits from `BaseSectionScorer`.
* **ExperienceClassificationResolver**: Decouples the scorer from Book 05 metadata representations. Maps matching details into internal enums.
* **ExperienceScoreValidator**: Read-only validator verifying presence of experience matches, absence of duplicates, and metadata validation constraints.
* **ExperienceScoringRules**: Configurations defining weights for exact, partial, overqualified, and underqualified matches, clamping boundaries, and partial matching settings.
* **BaseSectionScorer**: Shared abstract class unifying metadata dictionary properties and timing execution structures across all section scorers.
