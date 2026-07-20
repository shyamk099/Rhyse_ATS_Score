# Book 06 — ATS Scoring Engine
# Milestone 6.8 — Overall ATS Score Aggregation Engine

## Overview
Milestone 6.8 implements the **Overall ATS Score Aggregation Engine** — the final module in Book 06 that takes the SectionScore values (Skill, Experience, Education, Project, Certification) from the `ScoreResult` and aggregates them into a single, unified overall score between 0.0 and 100.0.

## Scope
This engine performs deterministic mathematical aggregation and normalization.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| OverallScoreAggregator | Recommendations |
| ScoreNormalizer | Explainability |
| SectionWeightConfiguration | AI / LLM / Embedding Scoring |
| AggregationValidator | Modifying section scorers |
| AggregationStatisticsBuilder | Modifying ScoreOrchestrator |
| Custom weight overrides | Business-specific hiring logic |

## How It Works
1. **Pre-Aggregation Validation**: Checks that all 5 section scores are present, contain numeric scores, and that weights total 100%.
2. **Normalization**: Every section score is normalized to [0.0, 100.0] via `(raw_score / maximum_score) * 100`.
3. **Weighting**: Computes weighted average:
   `Overall = (Skill * 0.35) + (Experience * 0.30) + (Education * 0.15) + (Project * 0.10) + (Certification * 0.10)`
4. **Clamping & Population**: Clamps final overall score to `[0.0, 100.0]`, builds aggregation stats, and returns a new immutable `ScoreResult` with `overall_score` populated.
