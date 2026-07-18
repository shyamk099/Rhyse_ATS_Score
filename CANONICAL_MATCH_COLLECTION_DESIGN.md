# Canonical Match Collection Design Specification

## 1. Goal & Context
The **Canonical Match Collection & Validation** module acts as the official gateway between **Book 05 (Matching Engine)** and all downstream scoring, recommendations, and explainability systems (Book 06+). It consolidates individual `MatchCollection` results (from Skill, Experience, Education, Project, and Certification matchers) into a single unified, validated, and immutable DTO: `CanonicalMatchCollection`.

---

## 2. Key Components
1. **CanonicalMatchCollectionService**: The public entry point exposing the `build()` API.
2. **CanonicalMatchCollectionPipeline**: Orchestrates the sequential stages of consolidation.
3. **MatchValidator**: Performs stateless structural integrity checks on individual matches.
4. **DuplicateMatchResolver**: Handles duplicate feature matches based on policies (`KEEP_FIRST`, `KEEP_LAST`, `KEEP_HIGHEST_CONFIDENCE`, `KEEP_ALL`).
5. **CrossMatchValidator**: Ensures cross-collection constraints (like unique match IDs).
6. **MatchStatisticsBuilder**: Compiles structural stats (match counts, warning/error counts, category counts).
7. **ValidationSummaryBuilder**: Consolidates validation outcomes.
8. **CanonicalMatchCollectionBuilder**: Deteriministically sorts and packages the final immutable collection.

---

## 3. Data Flow
```
[Skill Matches]
[Experience Matches]
[Education Matches]  ───> [CanonicalMatchCollectionPipeline] ───> [Validator] ───> [Resolver] ───> [CrossValidator] ───> [Final DTO]
[Project Matches]
[Certification Matches]
```
