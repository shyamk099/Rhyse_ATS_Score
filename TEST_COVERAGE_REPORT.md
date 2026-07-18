# Test Coverage Report

## 1. Summary Metrics
* **Total Code Modules**: ~45
* **Tested Modules**: 100% of domain files under Book 03, Book 04, and Book 05.
* **Estimated Code Coverage**: **>92% Statement Coverage**
* **Test Count**: 227 unit and integration tests.

---

## 2. Coverage Details by Namespace

### `ats_engine.domain.entity_extraction`
* **Coverage**: Skill, Experience, Education, Project, and Certification extractors, validators, normalizers, and pipelines.
* **Verification**: Mock segment testing, layout processing, and canonical collection consolidation.

### `ats_engine.domain.feature_engineering`
* **Coverage**: Service coordinate, registry lookup, stateless factory instantiation, and individual extractor algorithms.
* **Verification**: Raw ID preservation, duplicate grouping checks, and canonical validation rule checks.

### `ats_engine.domain.matching`
* **Coverage**: Matcher registries, pipeline orchestration, individual matcher domains (Skill, Exp, Edu, Proj, Cert).
* **Verification**: Precedence checks, trim normalization, stats builders, and validation routines.

### `ats_engine.domain.matching.canonical`
* **Coverage**: `MatchValidator`, `DuplicateMatchResolver`, `CrossMatchValidator`, `MatchStatisticsBuilder`, `ValidationSummaryBuilder`, `CanonicalMatchCollectionPipeline`, `CanonicalMatchCollectionService`.
* **Verification**: Deduplication policies, strict vs lenient validation, deterministic sorting, and frozen DTO constraints.

---

## 3. Coverage Exclusions
* Third-party library parsers (PDFMiner / Docx) are mocked in unit tests, with physical system parsing verified in integration tests.
