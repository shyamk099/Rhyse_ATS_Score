# Certification Extraction Component Diagram

## Book 03 — Entity Extraction | Milestone 3.8

```mermaid
graph TB
    subgraph "External Consumers"
        CLIENT["Client Code"]
    end

    subgraph "Certification Extraction Module"
        SERVICE["CertificationExtractionService<br/>(Public Facade)"]
        PIPELINE["CertificationExtractionPipeline<br/>(Orchestrator)"]

        subgraph "Processing Stages"
            CB["CertificationCandidateBuilder<br/>(Evidence Scanner)"]
            CV["CertificationCandidateValidator<br/>(Structure Check)"]
            NR["CertificationNormalizer<br/>(Field Cleaner)"]
            AS["CertificationAssembler<br/>(Record Grouper)"]
            EB["CertificationEntityBuilder<br/>(Confidence Scorer)"]
        end

        subgraph "Configuration"
            RULES["CertificationExtractionRules<br/>(Rule Engine Schema)"]
        end

        subgraph "Domain Models"
            CAND["CertificationCandidate"]
            NORM["NormalizedCertification"]
            ASMB["AssembledCertification"]
            ENT["CertificationEntity"]
            COLL["CertificationCollection"]
            STATS["CertificationExtractionStatistics"]
        end
    end

    subgraph "Upstream Dependencies"
        DOC["CanonicalDocument<br/>(Book 02)"]
        SEC["SectionCollection<br/>(Milestone 3.3)"]
        RE["Rule Engine<br/>(Milestone 1.4)"]
        LOG["LoggerFactory<br/>(Milestone 1.3)"]
    end

    CLIENT --> SERVICE
    SERVICE --> PIPELINE
    PIPELINE --> CB
    PIPELINE --> CV
    PIPELINE --> NR
    PIPELINE --> AS
    PIPELINE --> EB

    CB -.-> CAND
    CV -.-> CAND
    NR -.-> NORM
    AS -.-> ASMB
    EB -.-> ENT
    PIPELINE -.-> COLL
    COLL -.-> STATS

    SERVICE --> DOC
    SERVICE --> SEC
    SERVICE --> RE
    SERVICE --> LOG
    CB --> RULES
    CV --> RULES
    NR --> RULES
    AS --> RULES
    EB --> RULES

    style SERVICE fill:#4a90d9,stroke:#2c5f8a,color:#fff
    style PIPELINE fill:#5ba85b,stroke:#3d7a3d,color:#fff
    style CB fill:#e8a838,stroke:#b8842c,color:#fff
    style CV fill:#e8a838,stroke:#b8842c,color:#fff
    style NR fill:#e8a838,stroke:#b8842c,color:#fff
    style AS fill:#e8a838,stroke:#b8842c,color:#fff
    style EB fill:#e8a838,stroke:#b8842c,color:#fff
    style RULES fill:#9b59b6,stroke:#7d3c98,color:#fff
```
