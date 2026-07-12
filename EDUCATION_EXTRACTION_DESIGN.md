# Education Extraction Design Document

## Book 03 — Entity Extraction | Milestone 3.6

### Purpose

The Education Extraction engine is the second compound entity extractor in the Rhyse ATS system. Education records aggregate multiple correlated fields into a single structured record: institution name, degree, specialization/major, field of study, dates (raw), GPA/CGPA (raw), grade (raw), honors/distinction (raw), certifications (raw), and location (raw).

### Handbook Chapter

Book 03 — Entity Extraction (Education Extraction)

### Architecture

The module follows the standardized compound entity lifecycle pattern established in Milestone 3.5:

```
CanonicalDocument + SectionCollection
       ↓
EducationCandidateBuilder    (Scan segments for degree, institution, GPA, grade evidence)
       ↓
EducationCandidateValidator  (Require minimum structure: degree or institution)
       ↓
EducationNormalizer          (Split date pairs, detect graduation dates)
       ↓
EducationAssembler           (Group evidence, assign EDU-XXXXXXXX IDs, extract honors)
       ↓
EducationEntityBuilder       (Assign deterministic confidence and provenance)
       ↓
EducationCollection
```

### Design Decisions

#### 1. Raw Date Preservation
Dates are stored as raw text strings (`start_date_raw`, `end_date_raw`, `graduation_date_raw`). No date parsing or canonical date objects. Date interpretation belongs to Book 04.

#### 2. Configurable Indicators
Institution detection, degree detection, GPA patterns, grade patterns, major indicators, and honors indicators are all loaded from the Rule Engine. No hardcoded business vocabulary.

#### 3. Structured Collections
Honors and Certifications are stored as ordered tuples. Ordering and provenance are preserved.

#### 4. Canonical Education IDs
Every extracted education record receives a stable canonical identifier: `EDU-XXXXXXXX` (e.g., `EDU-00000001`).

#### 5. Assembler Never Fabricates
The `EducationAssembler` groups evidence only. Unknown values remain `None`.

#### 6. GPA vs CGPA
Both are stored as raw strings. No numeric parsing. The Rule Engine supplies `gpa_patterns` that match both formats.

#### 7. Graduation Date
If a graduation indicator is present alongside a single date, that date is treated as the graduation date. If two dates exist, the second serves as end date and graduation date when a graduation indicator is present.

### Dependencies

| Dependency | Source |
|---|---|
| `CanonicalDocument` | Book 02 — Document Processing |
| `SectionCollection` | Milestone 3.3 — Section Detection |
| `EducationExtractionRules` | Rule Engine Configuration |
| `LoggerFactory` | Infrastructure — Logging |

### Public API

```python
class EducationExtractionService:
    def extract_education(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> EducationCollection: ...
```

### Rule Engine Configuration

| Rule Category | Purpose |
|---|---|
| `institution_indicators` | Keywords identifying academic institutions |
| `degree_indicators` | Keywords identifying degree types |
| `major_indicators` | Keywords identifying specialization/major |
| `gpa_patterns` | Regex patterns for GPA/CGPA detection |
| `grade_patterns` | Regex patterns for grade/class detection |
| `honors_indicators` | Keywords identifying honors/distinction |
| `graduation_indicators` | Keywords indicating graduation |
| `date_patterns` | Regex patterns for date detection |
| `confidence_mappings` | Section-type → confidence weight mapping |
| `extraction_scope` | Which section types to scan |
