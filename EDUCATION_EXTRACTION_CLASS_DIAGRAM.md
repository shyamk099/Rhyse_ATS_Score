# Education Extraction Class Diagram

## Book 03 — Entity Extraction | Milestone 3.6

```mermaid
classDiagram
    class EducationExtractionService {
        -_logger: Logger
        +__init__(logger: Logger | None)
        +extract_education(document, sections, rule_engine_config) EducationCollection
    }

    class EducationExtractionPipeline {
        +execute(document, sections, rules)$ EducationCollection
    }

    class EducationCandidateBuilder {
        +build_candidates(document, sections, rules)$ Sequence~EducationCandidate~
        -_detect_institution(text, rules)$ str | None
        -_detect_degree(text, rules)$ str | None
        -_detect_major(text, rules)$ str | None
        -_detect_gpa(text, rules)$ str | None
        -_detect_grade(text, rules)$ str | None
    }

    class EducationCandidateValidator {
        +validate(candidate, rules)$ bool
    }

    class EducationNormalizer {
        +normalize(candidate, rules)$ NormalizedEducation
        -_split_dates(candidate, rules)$ tuple
    }

    class EducationAssembler {
        +assemble(normalized_list, rules)$ Sequence~AssembledEducation~
        -_extract_honors(raw_text, rules)$ list
        -_extract_certifications(raw_text)$ list
    }

    class EducationEntityBuilder {
        +build(assembled, rules)$ EducationEntity
    }

    class EducationExtractionRules {
        <<frozen>>
        +extraction_scope: Sequence~str~
        +date_patterns: Sequence~str~
        +graduation_indicators: Sequence~str~
        +institution_indicators: Sequence~str~
        +degree_indicators: Sequence~str~
        +major_indicators: Sequence~str~
        +gpa_patterns: Sequence~str~
        +grade_patterns: Sequence~str~
        +honors_indicators: Sequence~str~
        +confidence_mappings: Mapping~str, float~
        +default_confidence: float
    }

    class EducationCandidate {
        <<frozen>>
        +segment_id: str
        +section_type: str
        +raw_text: str
        +start_char: int
        +end_char: int
        +detected_dates: tuple~str~
        +detected_institution: str | None
        +detected_degree: str | None
        +detected_major: str | None
        +detected_gpa: str | None
        +detected_grade: str | None
        +has_graduation_indicator: bool
    }

    class NormalizedEducation {
        <<frozen>>
        +candidate: EducationCandidate
        +institution_name: str | None
        +degree: str | None
        +specialization: str | None
        +field_of_study: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +graduation_date_raw: str | None
        +gpa_raw: str | None
        +grade_raw: str | None
    }

    class AssembledEducation {
        <<frozen>>
        +education_id: str
        +institution_name: str | None
        +degree: str | None
        +specialization: str | None
        +field_of_study: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +graduation_date_raw: str | None
        +gpa_raw: str | None
        +grade_raw: str | None
        +honors: tuple~str~
        +certifications: tuple~str~
        +location_raw: str | None
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class EducationEntity {
        <<frozen>>
        +education_id: str
        +institution_name: str | None
        +degree: str | None
        +specialization: str | None
        +field_of_study: str | None
        +start_date_raw: str | None
        +end_date_raw: str | None
        +graduation_date_raw: str | None
        +gpa_raw: str | None
        +grade_raw: str | None
        +honors: tuple~str~
        +certifications: tuple~str~
        +location_raw: str | None
        +confidence: float
        +confidence_reason: str
        +matched_rules: tuple~str~
        +source_segment_ids: tuple~str~
        +source_text: str
    }

    class EducationCollection {
        <<frozen>>
        +entities: tuple~EducationEntity~
        +statistics: EducationExtractionStatistics
    }

    class EducationExtractionStatistics {
        <<frozen>>
        +total_education_records: int
        +records_with_degree: int
        +records_with_gpa: int
        +execution_duration_seconds: float
    }

    EducationExtractionService --> EducationExtractionPipeline : delegates
    EducationExtractionPipeline --> EducationCandidateBuilder : step 1
    EducationExtractionPipeline --> EducationCandidateValidator : step 2
    EducationExtractionPipeline --> EducationNormalizer : step 3
    EducationExtractionPipeline --> EducationAssembler : step 4
    EducationExtractionPipeline --> EducationEntityBuilder : step 5
    EducationCandidateBuilder ..> EducationCandidate : produces
    EducationNormalizer ..> NormalizedEducation : produces
    EducationAssembler ..> AssembledEducation : produces
    EducationEntityBuilder ..> EducationEntity : produces
    EducationExtractionPipeline ..> EducationCollection : returns
    EducationCollection --> EducationExtractionStatistics : contains
```
