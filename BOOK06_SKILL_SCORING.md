# Book 06 — ATS Scoring Engine | Milestone 6.2

## 1. Overview
This specification details the design and execution architecture for **Milestone 6.2 — Skill Scoring Engine**. The Skill Scoring Engine is responsible for executing deterministic score point calculations on Skill matches. It determines the mandatory or optional classification of each match via a classification resolver, accumulates weights, and returns a fully populated Skill section score complete with a detailed score breakdown.

---

## 2. Key Modules
* **SkillScorer**: Coordinates validations, classification resolving, raw point accumulation, clamping, and DTO construction.
* **SkillClassificationResolver**: Decouples the scorer from Book 05 metadata format variations by translating attributes into typed enums.
* **SkillScoreValidator**: Verifies that skill match results exist, contain no duplicates, and have valid metadata.
* **SkillScoringRules**: Defines parameters for strictness, weights, clamping boundaries, and partial match configurations.
* **ScoreBreakdown**: DTO segregating matched skills, missing skills, and mandatory/optional itemized counts.
