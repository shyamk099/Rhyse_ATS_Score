# Certification Extraction Sequence Diagram

## Book 03 — Entity Extraction | Milestone 3.8

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Service as CertificationExtractionService
    participant Pipeline as CertificationExtractionPipeline
    participant Builder as CertificationCandidateBuilder
    participant Validator as CertificationCandidateValidator
    participant Normalizer as CertificationNormalizer
    participant Assembler as CertificationAssembler
    participant EntityBuilder as CertificationEntityBuilder

    Client->>Service: extract_certification(doc, sections, config)
    Service->>Service: Load CertificationExtractionRules from config
    Service->>Pipeline: execute(doc, sections, rules)

    Pipeline->>Builder: build_candidates(doc, sections, rules)
    Builder->>Builder: Filter sections by extraction_scope
    Builder->>Builder: Scan segments for names, issuers, ID, URLs
    Builder-->>Pipeline: Sequence[CertificationCandidate]

    loop For each candidate
        Pipeline->>Validator: validate(candidate, rules)
        Validator-->>Pipeline: bool (has name or issuer)
    end

    loop For each validated candidate
        Pipeline->>Normalizer: normalize(candidate, rules)
        Normalizer->>Normalizer: Split dates into issue/expiration raw
        Normalizer->>Normalizer: Construct CertificationURL provenance objects
        Normalizer-->>Pipeline: NormalizedCertification
    end

    Pipeline->>Assembler: assemble(normalized_list, rules)
    Assembler->>Assembler: Assign canonical CERT-XXXXXXXX IDs
    Assembler->>Assembler: Resolve skills to Skill IDs / raw skills
    Assembler-->>Pipeline: Sequence[AssembledCertification]

    loop For each assembled record
        Pipeline->>EntityBuilder: build(assembled, rules)
        EntityBuilder->>EntityBuilder: Compute deterministic confidence
        EntityBuilder->>EntityBuilder: Generate confidence_reason
        EntityBuilder-->>Pipeline: CertificationEntity
    end

    Pipeline->>Pipeline: Compute CertificationExtractionStatistics
    Pipeline-->>Service: CertificationCollection
    Service-->>Client: CertificationCollection
```
