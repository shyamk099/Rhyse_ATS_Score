# Education Extraction Sequence Diagram

## Book 03 — Entity Extraction | Milestone 3.6

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Service as EducationExtractionService
    participant Pipeline as EducationExtractionPipeline
    participant Builder as EducationCandidateBuilder
    participant Validator as EducationCandidateValidator
    participant Normalizer as EducationNormalizer
    participant Assembler as EducationAssembler
    participant EntityBuilder as EducationEntityBuilder

    Client->>Service: extract_education(doc, sections, config)
    Service->>Service: Load EducationExtractionRules from config
    Service->>Pipeline: execute(doc, sections, rules)

    Pipeline->>Builder: build_candidates(doc, sections, rules)
    Builder->>Builder: Filter sections by extraction_scope
    Builder->>Builder: Scan segments for degrees, institutions, GPA, grades
    Builder-->>Pipeline: Sequence[EducationCandidate]

    loop For each candidate
        Pipeline->>Validator: validate(candidate, rules)
        Validator-->>Pipeline: bool (has degree or institution)
    end

    loop For each validated candidate
        Pipeline->>Normalizer: normalize(candidate, rules)
        Normalizer->>Normalizer: Split dates into start/end/graduation raw
        Normalizer-->>Pipeline: NormalizedEducation
    end

    Pipeline->>Assembler: assemble(normalized_list, rules)
    Assembler->>Assembler: Assign canonical EDU-XXXXXXXX IDs
    Assembler->>Assembler: Extract honors and certifications
    Assembler-->>Pipeline: Sequence[AssembledEducation]

    loop For each assembled record
        Pipeline->>EntityBuilder: build(assembled, rules)
        EntityBuilder->>EntityBuilder: Compute deterministic confidence
        EntityBuilder->>EntityBuilder: Generate confidence_reason
        EntityBuilder-->>Pipeline: EducationEntity
    end

    Pipeline->>Pipeline: Compute EducationExtractionStatistics
    Pipeline-->>Service: EducationCollection
    Service-->>Client: EducationCollection
```
