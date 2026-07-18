# Canonical Match Collection & Validation Implementation Plan

## Goal Description
Implement the final validation and consolidation layer for Book 05. This includes a service that builds an immutable `CanonicalMatchCollection` from the individual `MatchCollection`s (skill, experience, education, project, certification). The implementation must follow the strict architectural constraints, provide standardized telemetry, and expose a clean public API for downstream Books.

## User Review Required
> [!IMPORTANT]
> The new `CanonicalMatchCollection` is an immutable DTO that will become the sole input for Book 06 onward. Ensure that any existing code that may have been directly accessing individual `MatchCollection`s is updated to use the new service.
>
> The duplicate resolution policy must be chosen (e.g., `KEEP_FIRST`). Confirm the default you prefer.

## Open Questions
> [!WARNING] Confirm the desired default duplicate resolution strategy (KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL).
> 
> > Should the `CrossMatchValidator` enforce strict matcher category consistency (e.g., skill matches only contain matcher_type `SkillMatcher`)?
> 
> > What version identifier should be used for the `CanonicalMatchingRules` (e.g., `canonical_rules_v1.0`)?

## Proposed Changes
---
### matching/canonical
#### [NEW] [__init__.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/__init__.py)
Exports the public classes.

#### [NEW] [rules.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/rules.py)
Immutable Pydantic model defining configuration flags:
- `enabled: bool = True`
- `deterministic_ordering: bool = True`
- `duplicate_policy: Literal["KEEP_FIRST", "KEEP_LAST", "KEEP_HIGHEST_CONFIDENCE", "KEEP_ALL"] = "KEEP_FIRST"`
- `validation_mode: Literal["STRICT", "LENIENT"] = "STRICT"`
- `rules_version: str = "canonical_rules_v1.0"`

#### [NEW] [validator.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/validator.py)
Stateless `MatchValidator` that inspects each `MatchResult` for structural compliance (required fields, provenance, matcher_type consistency). Returns a list of `ValidationErrorDetail`.

#### [NEW] [duplicate_resolver.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/duplicate_resolver.py)
Resolves duplicate `MatchResult`s according to the configured `duplicate_policy`. Implements `keep_first`, `keep_last`, `keep_highest_confidence` (assumes a `confidence` attribute may be present), and `keep_all`.

#### [NEW] [cross_validator.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/cross_validator.py)
Validates cross‑collection invariants:
- No duplicate match IDs across collections.
- No duplicate resume feature IDs or job feature IDs across collections.
- All matcher_type values belong to the allowed set.
- Provenance fields are present.
Generates `ValidationWarningDetail` for non‑critical issues.

#### [NEW] [stats_builder.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/stats_builder.py)
Builds a `MatchStatistics` mapping using the standardized 8‑field schema (total matches, per‑category counts, duplicate counts, warning counts, validation_error_counts, execution_duration_ms, etc.).

#### [NEW] [validation_summary_builder.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/validation_summary_builder.py)
Aggregates `ValidationErrorDetail` and `ValidationWarningDetail` into a `ValidationSummary` model.

#### [NEW] [builder.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/builder.py)
Creates the immutable `CanonicalMatchCollection` DTO from sorted `MatchResult`s, statistics, and validation summary.

#### [NEW] [pipeline.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/pipeline.py)
Orchestrates the flow: validator → duplicate resolver → cross validator → stats builder → summary builder → collection builder. Returns the final collection.

#### [NEW] [service.py](file:///c:/Users/shyam/OneDrive/Desktop/Rhyse/Rhyse_ATS_Score/src/ats_engine/domain/matching/canonical/service.py)
Public API class `CanonicalMatchCollectionService` with the `build` method described in the spec. Delegates to `CanonicalMatchCollectionPipeline`.

---
### matching/models.py (modify)
Add immutable DTOs:
- `ValidationErrorDetail`
- `ValidationWarningDetail`
- `ValidationSummary`
- `MatchStatistics`
- `CanonicalMatchCollection`
All with `Config` set to `frozen = True, extra = "forbid"`.
Update imports where necessary.

### matching/exceptions.py (modify)
Append new typed exceptions:
- `MatchValidationError`
- `DuplicateMatchError`
- `CrossMatchValidationError`
- `CanonicalMatchCollectionBuildError`
All inherit from `Exception` and carry a message and optional payload.

---
### tests/unit/domain/test_canonical_match_collection.py (new)
Create comprehensive unit tests covering:
- Validation of a well‑formed collection (no errors).
- Detection of structural validation errors.
- Duplicate resolution according to each policy.
- Cross‑collection duplicate detection.
- Deterministic ordering of final collection.
- Immutability of the DTOs (attempting to modify raises `TypeError`).
- End‑to‑end pipeline integration.

---
### documentation (new artifacts)
Create markdown design artifacts in the artifacts directory:
- `CANONICAL_MATCH_COLLECTION_DESIGN.md`
- `CANONICAL_MATCH_COLLECTION_CLASS_DIAGRAM.md`
- `CANONICAL_MATCH_COLLECTION_SEQUENCE_DIAGRAM.md`
- `CANONICAL_MATCH_COLLECTION_COMPONENT_DIAGRAM.md`
- `CANONICAL_MATCH_COLLECTION_PACKAGE_DIAGRAM.md`
- `CANONICAL_MATCH_COLLECTION_DEPENDENCY_GRAPH.md`
- `BOOK05_COMPLETENESS_REPORT.md`
Update `IMPLEMENTATION_REPORT.md` to reference the new component.

## Verification Plan
1. **Static lint** – run `ruff`/`flake8` to ensure code style.
2. **Unit tests** – execute the command from the spec:
   ```powershell
   $env:PYTHONPATH="src"; python -m unittest discover -s tests -p "test_canonical_match_collection.py"
   ```
3. **Full suite** – run all tests to confirm no regressions.
4. **Manual inspection** – open the generated `CanonicalMatchCollection` in a REPL and verify ordering and immutability.
5. **Logging** – ensure the logger emits the consolidated statistics block with the expected keys.

**All processors remain stateless**, no global mutable state, and all DTOs are pure data containers.

---
**Implementation will proceed only after your approval.**
