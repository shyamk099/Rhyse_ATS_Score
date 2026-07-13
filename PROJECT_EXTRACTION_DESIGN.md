# Project Extraction Design Document

## Book 03 — Entity Extraction | Milestone 3.7

### Purpose

The Project Extraction engine extracts compound projects from resumes/JDs. Each Project entity is composed of several fields: Project Name, Organization/Client, Role, Start/End Dates (raw), Duration, Technologies (with canonical Skill ID reference integration), Responsibilities, Achievements, Description, Repository URL, Demo URL, and Location (raw).

### Handbook Chapter

Book 03 — Entity Extraction (Project Extraction)

### Architecture

The module follows the standardized compound entity lifecycle pattern established in Milestones 3.5 & 3.6:

```
CanonicalDocument + SectionCollection
       ↓
ProjectCandidateBuilder    (Scan segments for title, role, client, URL evidence)
       ↓
ProjectCandidateValidator  (Require minimum structure: project name or role)
       ↓
ProjectNormalizer          (Split date pairs, build ProjectURL provenance objects)
       ↓
ProjectAssembler           (Group evidence, map raw techs to Skill ID refs, assign PROJ-XXXXXXXX IDs)
       ↓
ProjectEntityBuilder       (Compute deterministic confidence and provenance)
       ↓
ProjectCollection
```

### Design Decisions

#### 1. Raw Date Preservation
Dates are stored as raw text strings (`start_date_raw`, `end_date_raw`, `duration_raw`). No date parsing or canonical date objects are built. Date interpretation belongs to Book 04.

#### 2. Configurable Heuristics
Heuristics for project titles, roles, clients/organizations, technology indicators, and repository/demo domains are loaded dynamically from the Rule Engine. No hardcoded business vocabulary is used.

#### 3. Structured Collections
Technologies, Responsibilities, and Achievements are stored as ordered tuples. Ordering and provenance are preserved.

#### 4. Canonical Project IDs
Every extracted project record receives a stable canonical identifier: `PROJ-XXXXXXXX` (e.g., `PROJ-00000001`).

#### 5. Skill ID Integration
Project technologies integrate with the canonical Skill model. When a project technology matches an existing canonical skill (configured in `technology_skill_mappings`), the canonical Skill ID reference is stored. Otherwise, the raw technology name is preserved.

#### 6. URL Provenance
Repository and Demo URLs are stored as structured `ProjectURL` objects which preserve the original value, normalized value (lowercase), and matched rule name (e.g. `repository_domain_github.com`), avoiding domain-collapse into a single string.

#### 7. Project Name Fallback Prevention
Project names are never inferred from repository or demo URLs. If no project name or title indicator is detected, the field remains null.

### Dependencies

| Dependency | Source |
|---|---|
| `CanonicalDocument` | Book 02 — Document Processing |
| `SectionCollection` | Milestone 3.3 — Section Detection |
| `ProjectExtractionRules` | Rule Engine Configuration |
| `LoggerFactory` | Infrastructure — Logging |

### Public API

```python
class ProjectExtractionService:
    def extract_project(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> ProjectCollection: ...
```
