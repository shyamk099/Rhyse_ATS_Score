# Experience Extraction Class Diagram

## Book 03 — Entity Extraction | Milestone 3.5

```mermaid
classDiagram
    class ExperienceExtractionService {
        -_logger: Logger
        +__init__(logger: Logger | None)
        +extract_experience(document, sections, rule_engine_config) ExperienceCollection
    }

    class ExperienceExtractionPipeline {
        +execute(document, sections, rules)$ ExperienceCollection
    }

    class ExperienceCandidateBuilder {
        +build_candidates(document, sections, rules)$ Sequence~ExperienceCandidate~
        -_detect_company(text, rules)$ str | None
        -_detect_title(text, rules)$ str | None
        -_detect_employment_type(text, rules)$ str | None
    }

    class ExperienceCandidateValidator {
        +validate(candidate, rules)$ bool
    }

    class ExperienceNormalizer {
        +normalize(candidate, rules)$ NormalizedExperience
        -_split_dates(candidate, rules)$ tuple
    }

    class ExperienceAssembler {
        +assemble(normalized_list, rules)$ Sequence~AssembledExperience~
        -_extract_structured_lists(raw_text)$ tuple
    }

    class ExperienceEntityBuilder {
        +build(assembled, rules)$ ExperienceEntity
    }

    class ExperienceExtractionRules {
        <<frozen>>
        +extraction_scope: Sequence~str~
        +date_patterns: Sequence~str~
        +current_employment_indicators: Sequence~str~
        +company_indicators: Sequence~str~
        +role_indicators: Sequence~str~
        +employment_type_mappings: Mapping~str, str~
        +date_range_separator: str
        +confidence_mappings: Mapping~str, float~
        +default_confidence: float
    }

    class ExperienceCandidate {
        <<frozen>>
        +segment_id: str
        +section_type: str
        +raw_text: str
        +start_char: int
        +end_char: int
        +detected_dates: tuple~str~
        +detected_company: str | None
        +detected_title: str | None
        +detected_employment_type: str | None
        +is_current: bool
    }

    class NormalizedExperience {
        <<frozen>>
        +candidate: ExperienceCandidate
        +company_name: str | None
        +job_title: str | None
        +employment_type: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +is_current: bool
    }

    class AssembledExperience {
        <<frozen>>
        +experience_id: str
        +company_name: str | None
        +job_title: str | None
        +employment_type: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +is_current: bool
        +responsibilities: tuple~str~
        +technologies: tuple~str~
        +achievements: tuple~str~
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class ExperienceEntity {
        <<frozen>>
        +experience_id: str
        +company_name: str | None
        +job_title: str | None
        +employment_type: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +is_current: bool
        +responsibilities: tuple~str~
        +technologies: tuple~str~
        +achievements: tuple~str~
        +confidence: float
        +confidence_reason: str
        +matched_rules: tuple~str~
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class ExperienceCollection {
        <<frozen>>
        +entities: tuple~ExperienceEntity~
        +statistics: ExperienceExtractionStatistics
    }

    class ExperienceExtractionStatistics {
        <<frozen>>
        +total_experiences: int
        +current_employment_count: int
        +execution_duration_seconds: float
    }

    ExperienceExtractionService --> ExperienceExtractionPipeline : delegates
    ExperienceExtractionPipeline --> ExperienceCandidateBuilder : step 1
    ExperienceExtractionPipeline --> ExperienceCandidateValidator : step 2
    ExperienceExtractionPipeline --> ExperienceNormalizer : step 3
    ExperienceExtractionPipeline --> ExperienceAssembler : step 4
    ExperienceExtractionPipeline --> ExperienceEntityBuilder : step 5
    ExperienceCandidateBuilder ..> ExperienceCandidate : produces
    ExperienceNormalizer ..> NormalizedExperience : produces
    ExperienceAssembler ..> AssembledExperience : produces
    ExperienceEntityBuilder ..> ExperienceEntity : produces
    ExperienceExtractionPipeline ..> ExperienceCollection : returns
    ExperienceCollection --> ExperienceExtractionStatistics : contains
```
