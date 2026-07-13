# Canonical Entity Collection Sequence Diagram

## Book 03 — Entity Extraction | Milestone 3.9

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Service as CanonicalEntityCollectionService
    participant Pipeline as CanonicalEntityCollectionPipeline
    participant Validator as EntityValidator
    participant Resolver as DuplicateResolver
    participant XRef as CrossReferenceValidator

    Client->>Service: build(contacts, skills, experiences, education, projects, certifications, config)
    Service->>Service: Load CanonicalValidationRules from config
    Service->>Pipeline: execute(contacts, skills, experiences, education, projects, certifications, rules)

    Pipeline->>Validator: validate(contacts, skills, experiences, education, projects, certifications, rules)
    Validator->>Validator: Check empty required collections, duplicate IDs, URL formats, provenance bounds
    Validator-->>Pipeline: Sequence[ValidationErrorDetail] (structural)

    Pipeline->>Resolver: resolve(experiences.entities, rules, key_field="experience_id")
    Resolver-->>Pipeline: Sequence[ExperienceEntity] (deduplicated)
    Pipeline->>Resolver: resolve(education.entities, rules, key_field="education_id")
    Resolver-->>Pipeline: Sequence[EducationEntity] (deduplicated)
    Pipeline->>Resolver: resolve(projects.entities, rules, key_field="project_id")
    Resolver-->>Pipeline: Sequence[ProjectEntity] (deduplicated)
    Pipeline->>Resolver: resolve(certifications.entities, rules, key_field="certification_id")
    Resolver-->>Pipeline: Sequence[CertificationEntity] (deduplicated)

    Pipeline->>Pipeline: Compile deduplicated collections

    Pipeline->>XRef: validate(skills, experiences, projects, certifications, rules)
    XRef->>XRef: Check that referenced Skill IDs exist in SkillCollection
    XRef-->>Pipeline: Sequence[ValidationErrorDetail] (references)

    Pipeline->>Pipeline: Build ValidationSummary and EntityStatistics
    Pipeline-->>Service: CanonicalEntityCollection
    Service-->>Client: CanonicalEntityCollection
```
