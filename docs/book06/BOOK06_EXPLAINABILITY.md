# Book 06 — ATS Scoring Engine
# Milestone 6.9 — Deterministic Score Explainability Engine

## Overview
Milestone 6.9 implements the **Score Explainability Engine** — the module that interprets a finished `ScoreResult` and creates mathematically detailed, structural explainability DTOs containing formatted formulas and summaries.

## Scope
This engine performs deterministic generation of equations and explanations.

| ✅ Implemented | ❌ Explicitly Excluded |
|---|---|
| ExplainabilityEngine | Recommendations / Career Advice |
| SectionExplanation DTO | Resume suggestions |
| OverallExplanation DTO | Suggestions for improvements |
| ExplainabilityResult wrapper DTO | AI / LLM / NLG (natural-language generation) |
| Formatter & Builders | Modifying any scoring algorithm |
| Optional overall score validation | Inspecting MatchResults directly |

## How It Works
1. **Explainability Validation**: Inspects the incoming `ScoreResult` to make sure all 5 section score fields are present and contain valid scores.
2. **Flexible Overall Score Checking**: If `overall_score` is populated, generates an `OverallExplanation`. If it is absent (None), `overall_explanation` is set to None.
3. **Section Explanations**: For every section, maps the matched/missing items list, builds the exact mathematical calculation string, and constructs a `SectionExplanation` DTO.
4. **Formula Formatter**: Translates fractions and weights into formatting sequences:
   - Section: `(raw_score / maximum_score) × 100 × weight_used = contribution`
   - Overall: `overall_score = skill_contrib + experience_contrib + education_contrib + project_contrib + certification_contrib`
