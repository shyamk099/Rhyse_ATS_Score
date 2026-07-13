# Project Extraction Sequence Diagram

## Book 03 — Entity Extraction | Milestone 3.7

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Service as ProjectExtractionService
    participant Pipeline as ProjectExtractionPipeline
    participant Builder as ProjectCandidateBuilder
    participant Validator as ProjectCandidateValidator
    participant Normalizer as ProjectNormalizer
    participant Assembler as ProjectAssembler
    participant EntityBuilder as ProjectEntityBuilder

    Client->>Service: extract_project(doc, sections, config)
    Service->>Service: Load ProjectExtractionRules from config
    Service->>Pipeline: execute(doc, sections, rules)

    Pipeline->>Builder: build_candidates(doc, sections, rules)
    Builder->>Builder: Filter sections by extraction_scope
    Builder->>Builder: Scan segments for name, role, URLs, dates
    Builder-->>Pipeline: Sequence[ProjectCandidate]

    loop For each candidate
        Pipeline->>Validator: validate(candidate, rules)
        Validator-->>Pipeline: bool (has name or role)
    end

    loop For each validated candidate
        Pipeline->>Normalizer: normalize(candidate, rules)
        Normalizer->>Normalizer: Split dates into start/end raw
        Normalizer->>Normalizer: Construct ProjectURL provenance objects
        Normalizer-->>Pipeline: NormalizedProject
    end

    Pipeline->>Assembler: assemble(normalized_list, rules)
    Assembler->>Assembler: Assign canonical PROJ-XXXXXXXX IDs
    Assembler->>Assembler: Resolve technologies to Skill IDs
    Assembler->>Assembler: Extract structured lists (responsibilities, achievements)
    Assembler-->>Pipeline: Sequence[AssembledProject]

    loop For each assembled record
        Pipeline->>EntityBuilder: build(assembled, rules)
        EntityBuilder->>EntityBuilder: Compute deterministic confidence
        EntityBuilder->>EntityBuilder: Generate confidence_reason and offsets
        EntityBuilder-->>Pipeline: ProjectEntity
    end

    Pipeline->>Pipeline: Compute ProjectExtractionStatistics
    Pipeline-->>Service: ProjectCollection
    Service-->>Client: ProjectCollection
```
