# Education Matching Class Diagram

## Book 05 — Matching Engine | Milestone 5.4

The class diagram outlines interfaces and helper classes supporting `EducationMatcher`:

```mermaid
classDiagram
    class FeatureMatcher {
        <<interface>>
        +match(resume_features, job_features, context) Sequence~MatchResult~
    }

    class EducationMatcher {
        -_logger: Logger
        -_validator: EducationMatchValidator
        -_normalizer: EducationMatchNormalizer
        +match(resume_features, job_features, context) Sequence~MatchResult~
    }

    class EducationMatchCandidateBuilder {
        +build_candidates(resume_features, job_features, rules) Sequence~EducationMatchCandidate~
        -_is_empty_education(feature) bool
    }

    class EducationMatchCandidate {
        +resume_feature: Feature
        +job_feature: Feature
    }

    class EducationMatchValidator {
        -_logger: Logger
        +validate(candidate, rules) list~str~
    }

    class EducationMatchNormalizer {
        +normalize(candidate, rules) EducationMatchCandidate
    }

    class EducationMatchBuilder {
        +build(candidate, context) MatchResult
    }

    class CommonComparison {
        +safe_compare_strings(str1, str2) bool
        +compare_matching_fields(val1, val2, fields) bool
    }

    FeatureMatcher <|-- EducationMatcher
    EducationMatcher --> EducationMatchCandidateBuilder
    EducationMatcher --> EducationMatchValidator
    EducationMatcher --> EducationMatchNormalizer
    EducationMatcher --> EducationMatchBuilder
    EducationMatcher --> CommonComparison
    EducationMatchCandidateBuilder --> EducationMatchCandidate
```
