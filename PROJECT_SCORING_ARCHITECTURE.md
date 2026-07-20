# Project Scoring Architecture

## 1. Pipeline Ingestion & Translation Diagram
```
   [Project MatchResults] ──> [ProjectClassificationResolver] ──> [ProjectScorer Point Calculator] ──> [ScoreBreakdown]
```

## 2. Calculation Logic
1. **Validation**: Check collection mappings, absence of duplicates, and valid metadata using `ProjectScoreValidator`.
2. **Classification**: Match result properties are adapted into type-safe enums (`EXACT_MATCH`, `SIMILAR_PROJECT`, `RELATED_PROJECT`, `PARTIAL_MATCH`, `NO_MATCH`) by `ProjectClassificationResolver` (inherits from generic `AbstractClassificationResolver`).
3. **Weight Accumulation**:
   $$\text{Raw Points} = (N_{\text{exact}} \times 3.0) + (N_{\text{similar}} \times 2.5) + (N_{\text{related}} \times 2.0) + (N_{\text{partial}} \times 1.0) + (N_{\text{no\_match}} \times 0.0)$$
4. **Clamping Boundary**: Clamps the accumulated value between `minimum_project_score` (default: 0.0) and `maximum_project_score` (default: 15.0).
5. **Generic Breakdown compiling**: Organizes matched items, missing items, and classification counts in the unified `ScoreBreakdown` DTO.
