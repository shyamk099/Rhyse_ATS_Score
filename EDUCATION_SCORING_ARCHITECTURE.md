# Education Scoring Architecture

## 1. Pipeline Ingestion & Translation Diagram
```
   [Education MatchResults] ──> [EducationClassificationResolver] ──> [EducationScorer Point Calculator] ──> [ScoreBreakdown]
```

## 2. Calculation Logic
1. **Validation**: Check collection mappings, absence of duplicates, and valid metadata using `EducationScoreValidator`.
2. **Classification**: Match result properties are adapted into type-safe enums (`EXACT_MATCH`, `HIGHER_THAN_REQUIRED`, `LOWER_THAN_REQUIRED`, `RELATED_FIELD`, `UNRELATED_FIELD`, `NO_MATCH`) by `EducationClassificationResolver` (inherits from generic `AbstractClassificationResolver`).
3. **Weight Accumulation**:
   $$\text{Raw Points} = (N_{\text{exact}} \times 4.0) + (N_{\text{higher}} \times 4.0) + (N_{\text{related}} \times 2.5) + (N_{\text{lower}} \times 1.0) + (N_{\text{unrelated}} \times 0.0)$$
4. **Clamping Boundary**: Clamps the accumulated value between `minimum_education_score` (default: 0.0) and `maximum_education_score` (default: 15.0).
5. **Generic Breakdown compiling**: Organizes matched items, missing items, and classification counts in the unified `ScoreBreakdown` DTO.
