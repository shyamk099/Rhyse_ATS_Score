# Experience Scoring Architecture

## 1. Pipeline Ingestion & Translation Diagram
```
   [Experience MatchResults] ──> [ExperienceClassificationResolver] ──> [ExperienceScorer Point Calculator] ──> [ScoreBreakdown]
```

## 2. Calculation Logic
1. **Validation**: Check collection mappings, absence of duplicates, and valid metadata using `ExperienceScoreValidator`.
2. **Classification**: Match result properties are adapted into type-safe enums (`EXACT_MATCH`, `PARTIAL_MATCH`, `OVERQUALIFIED`, `UNDERQUALIFIED`, `NO_MATCH`) by `ExperienceClassificationResolver`.
3. **Weight Accumulation**:
   $$\text{Raw Points} = (N_{\text{exact}} \times w_{\text{exact}}) + (N_{\text{partial}} \times w_{\text{partial}}) + (N_{\text{overqualified}} \times w_{\text{overqualified}}) + (N_{\text{underqualified}} \times w_{\text{underqualified}})$$
4. **Clamping Boundary**: Clamps the accumulated value between `minimum_experience_score` (default: 0.0) and `maximum_experience_score` (default: 25.0).
5. **Generic Breakdown compiling**: Organizes matched items, missing items, and classification counts in the unified `ScoreBreakdown` DTO.
