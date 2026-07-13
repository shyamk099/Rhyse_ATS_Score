# Certification Extraction Design Document

## Book 03 — Entity Extraction | Milestone 3.8

### Purpose

The Certification Extraction engine parses compound certifications from resume/JD layout segments. Each Certification entity aggregates: Certification Name, Issuing Organization, Credential ID, Credential URL, Issue Date, Expiration Date, Validity Status (raw), Associated Skill IDs, Associated Skills (raw), and Description (raw).

### Handbook Chapter

Book 03 — Entity Extraction (Certification Extraction)

### Architecture

The module follows the standardized compound entity lifecycle pattern established in Milestones 3.5 — 3.7:

```
CanonicalDocument + SectionCollection
       ↓
CertificationCandidateBuilder    (Scan segments for name, issuer, credential ID, URL evidence)
       ↓
CertificationCandidateValidator  (Require minimum structure: name or issuing organization)
       ↓
CertificationNormalizer          (Split date pairs, build CertificationURL provenance objects)
       ↓
CertificationAssembler           (Group evidence, map raw skills to Skill ID refs, assign CERT-XXXXXXXX IDs)
       ↓
CertificationEntityBuilder       (Compute deterministic confidence and provenance)
       ↓
CertificationCollection
```

### Design Decisions

#### 1. Raw Date Preservation
Dates are stored as raw text strings (`issue_date_raw`, `expiration_date_raw`). No date parsing or canonical date objects are built. Date interpretation belongs to Book 04.

#### 2. Configurable Heuristics
Heuristics for certification indicators, issuers/organizations, credential URL/ID regex patterns, and skill mappings are loaded dynamically from the Rule Engine. No hardcoded business vocabulary is used.

#### 3. Structured Collections
Associated Skill IDs and Raw Skills are stored as ordered tuples. Ordering and provenance are preserved.

#### 4. Canonical Certification IDs
Every extracted certification record receives a stable canonical identifier: `CERT-XXXXXXXX` (e.g., `CERT-00000001`).

#### 5. Skill ID Integration
Certification skills integrate with the canonical Skill model. When an associated skill maps to an existing Skill ID, the canonical Skill ID reference is stored. Otherwise, the raw skill term is preserved.

#### 6. URL Provenance
Credential URLs are stored as structured `CertificationURL` objects which preserve the original value, normalized value (lowercase), and matched rule name, avoiding domain-collapse.

#### 7. Raw Validity Status
Validity status is kept strictly raw. No active, expired, or validation checks are computed in Book 03. Interpretation belongs to Book 04.

### Dependencies

| Dependency | Source |
|---|---|
| `CanonicalDocument` | Book 02 — Document Processing |
| `SectionCollection` | Milestone 3.3 — Section Detection |
| `CertificationExtractionRules` | Rule Engine Configuration |
| `LoggerFactory` | Infrastructure — Logging |

### Public API

```python
class CertificationExtractionService:
    def extract_certification(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> CertificationCollection: ...
```
