# Scoring Architecture Specification

## 1. Context Diagram
```
   [Book 05 Matching] ──(CanonicalMatchCollection)──> [Book 06 Scoring Engine] ──(ScoreResult)──> [Downstream Systems]
```

## 2. Ingestion-to-Score Lifecycle
1. **Request Ingestion**: `ScoringService` receives the consolidated `CanonicalMatchCollection` and the `ScoringRules` payload.
2. **Validation Stage**: `ScoreValidator` performs strict, read-only checks to ensure matching categories are supported and rules versions are compatible.
3. **Execution Stage**: Active scorers resolved from `ScoringRegistry` are sorted by priority and sequentially executed inside `ScoringPipeline`.
4. **Assembly Stage**: Context is populated with section scores; `ScoreStatistics` and `ScoreMetadata` are compiled.
5. **Output Generation**: An immutable, frozen `ScoreResult` is returned to the client containing section placeholders.
