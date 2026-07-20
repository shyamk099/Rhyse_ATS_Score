# Skill Scoring Architecture

## 1. Pipeline Ingestion & Translation Diagram
```
   [Skill MatchResults] ──> [SkillClassificationResolver] ──> [SkillScorer Point Calculator] ──> [ScoreBreakdown]
```

## 2. Calculation Logic
1. **Validation**: Check collection result mappings and metadata using `SkillScoreValidator`.
2. **Classification**: Match result properties are adapted into type-safe enums (`MANDATORY`, `OPTIONAL`) by `SkillClassificationResolver`.
3. **Weight Accumulation**:
   $$\text{Raw Points} = (\text{Mandatory Matches} \times \text{mandatory\_skill\_weight}) + (\text{Optional Matches} \times \text{optional\_skill\_weight})$$
4. **Clamping Boundary**: Clamps the accumulated value between `minimum_skill_score` (default: 0.0) and `maximum_skill_score` (default: 40.0).
5. **Breakdown compiling**: Organizes results, missing items, and stats counts into the finalized `SectionScore`.
