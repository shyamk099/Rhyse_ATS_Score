# Contact Information Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.2 — Contact Information Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the contact information extraction module.

---

# Architecture

```mermaid
classDiagram
    class ContactInformationExtractor {
        +extract(segment: DocumentSegment, context: EntityExtractionContext) Sequence~ExtractedEntity~
    }

    class PatternCandidateBuilder {
        +find_candidates(text: str, rules: ContactExtractionRules) Sequence~ContactCandidate~
    }

    class CandidateValidator {
        +validate_candidate(candidate: ContactCandidate) bool
    }

    class ContactNormalizer {
        +normalize(value: str, entity_type: str) str
    }

    class ContactEntityBuilder {
        +build(candidate: ContactCandidate, normalized_value: str, segment_id: str, rules: ContactExtractionRules) ExtractedEntity
    }

    class ContactExtractionRules {
        +email_pattern: str
        +phone_pattern: str
        +linkedin_pattern: str
        +github_pattern: str
        +portfolio_pattern: str
        +email_confidence: float
        +phone_confidence: float
        +linkedin_confidence: float
        +github_confidence: float
        +portfolio_confidence: float
    }

    class ContactCandidate {
        +value: str
        +entity_type: str
        +start_char: int
        +end_char: int
    }

    ContactInformationExtractor --> PatternCandidateBuilder : uses
    ContactInformationExtractor --> CandidateValidator : uses
    ContactInformationExtractor --> ContactNormalizer : uses
    ContactInformationExtractor --> ContactEntityBuilder : uses
    ContactInformationExtractor ..> ContactExtractionRules : consumes
    PatternCandidateBuilder ..> ContactCandidate : compiles
    ContactEntityBuilder ..> ContactCandidate : consumes
```
