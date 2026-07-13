# Certification Extraction Class Diagram

## Book 03 — Entity Extraction | Milestone 3.8

```mermaid
classDiagram
    class CertificationExtractionService {
        -_logger: Logger
        +__init__(logger: Logger | None)
        +extract_certification(document, sections, rule_engine_config) CertificationCollection
    }

    class CertificationExtractionPipeline {
        +execute(document, sections, rules)$ CertificationCollection
    }

    class CertificationCandidateBuilder {
        +build_candidates(document, sections, rules)$ Sequence~CertificationCandidate~
        -_detect_name(text, rules)$ str | None
        -_detect_issuer(text, rules)$ str | None
    }

    class CertificationCandidateValidator {
        +validate(candidate, rules)$ bool
    }

    class CertificationNormalizer {
        +normalize(candidate, rules)$ NormalizedCertification
        -_split_dates(candidate, rules)$ tuple
    }

    class CertificationAssembler {
        +assemble(normalized_list, rules)$ Sequence~AssembledCertification~
        -_extract_skills(raw_text, rules)$ tuple
        -_extract_description(raw_text)$ str | None
    }

    class CertificationEntityBuilder {
        +build(assembled, rules)$ CertificationEntity
    }

    class CertificationExtractionRules {
        <<frozen>>
        +extraction_scope: Sequence~str~
        +date_patterns: Sequence~str~
        +certification_indicators: Sequence~str~
        +issuing_organization_indicators: Sequence~str~
        +credential_url_patterns: Sequence~str~
        +credential_id_patterns: Sequence~str~
        +skill_mappings: Mapping~str, str~
        +confidence_mappings: Mapping~str, float~
        +default_confidence: float
    }

    class CertificationCandidate {
        <<frozen>>
        +segment_id: str
        +section_type: str
        +raw_text: str
        +start_char: int
        +end_char: int
        +detected_dates: tuple~str~
        +detected_name: str | None
        +detected_issuer: str | None
        +detected_credential_id: str | None
        +detected_credential_url: str | None
    }

    class NormalizedCertification {
        <<frozen>>
        +candidate: CertificationCandidate
        +certification_name: str | None
        +issuing_organization: str | None
        +credential_id_raw: str | None
        +credential_url: CertificationURL | None
        +issue_date_raw: str | None
        +expiration_date_raw: str | None
        +validity_status_raw: str | None
    }

    class AssembledCertification {
        <<frozen>>
        +certification_id: str
        +certification_name: str | None
        +issuing_organization: str | None
        +credential_id_raw: str | None
        +credential_url: CertificationURL | None
        +issue_date_raw: str | None
        +expiration_date_raw: str | None
        +validity_status_raw: str | None
        +associated_skill_ids: tuple~str~
        +associated_skills_raw: tuple~str~
        +description_raw: str | None
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class CertificationEntity {
        <<frozen>>
        +certification_id: str
        +certification_name: str | None
        +issuing_organization: str | None
        +credential_id_raw: str | None
        +credential_url: CertificationURL | None
        +issue_date_raw: str | None
        +expiration_date_raw: str | None
        +validity_status_raw: str | None
        +associated_skill_ids: tuple~str~
        +associated_skills_raw: tuple~str~
        +description_raw: str | None
        +confidence: float
        +confidence_reason: str
        +matched_rules: tuple~str~
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class CertificationURL {
        <<frozen>>
        +original_value: str
        +normalized_value: str
        +matched_rule: str
    }

    class CertificationCollection {
        <<frozen>>
        +entities: tuple~CertificationEntity~
        +statistics: CertificationExtractionStatistics
    }

    class CertificationExtractionStatistics {
        <<frozen>>
        +total_certifications: int
        +active_certifications: int
        +execution_duration_seconds: float
    }

    CertificationExtractionService --> CertificationExtractionPipeline : delegates
    CertificationExtractionPipeline --> CertificationCandidateBuilder : step 1
    CertificationExtractionPipeline --> CertificationCandidateValidator : step 2
    CertificationExtractionPipeline --> CertificationNormalizer : step 3
    CertificationExtractionPipeline --> CertificationAssembler : step 4
    CertificationExtractionPipeline --> CertificationEntityBuilder : step 5
    CertificationCandidateBuilder ..> CertificationCandidate : produces
    CertificationNormalizer ..> NormalizedCertification : produces
    CertificationAssembler ..> AssembledCertification : produces
    CertificationEntityBuilder ..> CertificationEntity : produces
    AssembledCertification --> CertificationURL : contains
    CertificationEntity --> CertificationURL : contains
    CertificationExtractionPipeline ..> CertificationCollection : returns
    CertificationCollection --> CertificationExtractionStatistics : contains
```
