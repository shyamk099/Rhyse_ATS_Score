# Canonical Entity Collection Design Document

## Book 03 — Entity Extraction | Milestone 3.9

### Purpose

The Canonical Entity Collection acts as the consolidated DTO representing the aggregate of all extracted entities in Book 03 (Contacts, Skills, Experiences, Education, Projects, and Certifications). It is the sole output contract for Book 03 and the sole input contract for Book 04 (Feature Engineering), establishing a clean, decoupling boundary.

### Handbook Chapter

Book 03 — Entity Extraction (Entity Validation & Canonical Entity Collection)

### Architecture

The module runs a sequential pipeline to validate structural integrity, resolve duplicates, verify cross-references, and output statistics:

```
Entity collections (Contact, Skill, Experience, Education, Project, Certification) + Rules
                                   ↓
                       EntityValidationPipeline
                                   ↓
          EntityValidator (verify non-empty, duplicate IDs, URL formats)
                                   ↓
          DuplicateResolver (deduplicate entities based on merge/conflict rules)
                                   ↓
          CrossReferenceValidator (verify Project/Cert Skill IDs exist in Skills)
                                   ↓
                       CanonicalEntityCollection
```

### Design Decisions

#### 1. Pure Immutable DTO
`CanonicalEntityCollection` is a pure data transfer object with no helper methods, lookups, or logic. It is defined as a frozen Pydantic model (`frozen=True`, `extra="forbid"`).

#### 2. Read-Only Validation
Validators only inspect, verify, and report. They never repair, normalize, infer, or modify entities.

#### 3. Structured Explainability
The `ValidationSummary` includes detailed validation details containing `status` ("VALID" or "INVALID"), `errors`, `warnings`, `duplicate_count`, `reference_errors`, `validation_timestamp`, and `rules_version`.

#### 4. Structural Metrics only
`EntityStatistics` contains only structural counts and metrics (e.g. `duplicate_count`, `validation_error_count`, entity counts). No semantic scores or downstream features are calculated here.

#### 5. Skill Reference Decoupling
Cross-referencing prevents broken links between compound extractors (like Project or Certification) and Skill Collections. The validation engine strictly reports broken links without trying to resolve them automatically.

### Dependencies

| Dependency | Source |
|---|---|
| All individual collections | Milestones 3.2 — 3.8 |
| `CanonicalValidationRules` | Rule Engine Configuration |
| `LoggerFactory` | Infrastructure — Logging |

### Public API

```python
class CanonicalEntityCollectionService:
    def build(
        self,
        contacts: EntityCollection,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        education: EducationCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> CanonicalEntityCollection: ...
```
