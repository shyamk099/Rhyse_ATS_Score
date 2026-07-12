# Experience Extraction Design Document

## Book 03 — Entity Extraction | Milestone 3.5

### Purpose

The Experience Extraction engine is the first compound entity extractor in the Rhyse ATS system. Unlike atomic entities (Email, Phone, Skill), Experience records aggregate multiple correlated fields into a single structured record: company name, job title, employment type, dates, responsibilities, technologies, and achievements.

### Handbook Chapter

Book 03 — Entity Extraction (Experience Extraction)

### Architecture

The module follows the approved Entity Extraction Foundation pipeline pattern:

```
CanonicalDocument + SectionCollection
       ↓
ExperienceCandidateBuilder    (Scan segments for date, company, role evidence)
       ↓
ExperienceCandidateValidator  (Require minimum structure: title or company)
       ↓
ExperienceNormalizer          (Normalize employment types, split date pairs)
       ↓
ExperienceAssembler           (Group evidence into compound records with canonical IDs)
       ↓
ExperienceEntityBuilder       (Assign deterministic confidence and provenance)
       ↓
ExperienceCollection
```

### Design Decisions

#### 1. Raw Date Preservation
Dates are stored as raw text strings (`start_date_raw`, `end_date_raw`). No date parsing or canonical date objects are introduced. Date interpretation belongs to Book 04 — Feature Engineering.

#### 2. Configurable Company Detection
Company detection uses configurable company indicators supplied by the Rule Engine. The detection strategy is regex-based but replaceable. No hardcoded assumptions about organization names exist.

#### 3. Structured Collections
Responsibilities, Technologies, and Achievements are stored as ordered tuples — never concatenated into text blobs. Provenance and ordering are preserved.

#### 4. Canonical Experience IDs
Every extracted experience record receives a stable canonical identifier following the pattern `EXP-XXXXXXXX` (e.g., `EXP-00000001`). This enables clean downstream references from Feature Engineering, Evidence Intelligence, and ATS Scoring.

#### 5. Assembler Never Fabricates
The `ExperienceAssembler` groups evidence only. Unknown values remain `None`. No synthetic data is injected.

#### 6. Deterministic Confidence
Confidence is computed from matched component signals (company, title, dates, responsibilities) scaled by section-level weighting from the Rule Engine configuration.

### Dependencies

| Dependency | Source |
|---|---|
| `CanonicalDocument` | Book 02 — Document Processing |
| `SectionCollection` | Milestone 3.3 — Section Detection |
| `ExperienceExtractionRules` | Rule Engine Configuration |
| `LoggerFactory` | Infrastructure — Logging |

### Public API

```python
class ExperienceExtractionService:
    def extract_experience(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> ExperienceCollection: ...
```

### Rule Engine Configuration

| Rule Category | Purpose |
|---|---|
| `company_indicators` | Suffixes/keywords identifying organization names |
| `role_indicators` | Keywords identifying job titles and seniority |
| `employment_type_mappings` | Raw text → canonical employment type mapping |
| `date_patterns` | Regex patterns for date detection |
| `current_employment_indicators` | Keywords marking current employment |
| `confidence_mappings` | Section-type → confidence weight mapping |
| `extraction_scope` | Which section types to scan |
