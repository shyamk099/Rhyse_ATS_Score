# Skill Extraction Class Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.4 — Skill Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the class diagram for the skill extraction module.

---

# Architecture

```mermaid
classDiagram
    class SkillExtractionService {
        -_pipeline: SkillExtractionPipeline
        -_logger: Logger
        +extract_skills(document: CanonicalDocument, sections: SectionCollection, rule_engine_config: Mapping) SkillCollection
    }

    class SkillExtractionPipeline {
        -_builder: SkillCandidateBuilder
        +execute(document: CanonicalDocument, sections: SectionCollection, rules: SkillExtractionRules) SkillCollection
    }

    class SkillCandidateBuilder {
        -_matcher: SkillMatcher
        +build_candidates(document: CanonicalDocument, sections: SectionCollection, rules: SkillExtractionRules) Sequence~SkillCandidate~
    }

    class SkillMatcher {
        <<interface>>
        +match(segment: DocumentSegment, rules: SkillExtractionRules, section_type: str) Sequence~SkillCandidate~
    }

    class DictionaryMatcher {
        +match(segment: DocumentSegment, rules: SkillExtractionRules, section_type: str) Sequence~SkillCandidate~
    }

    class SkillCandidateValidator {
        +validate(candidate: SkillCandidate, rules: SkillExtractionRules) bool
    }

    class SkillNormalizer {
        +normalize(candidate: SkillCandidate, rules: SkillExtractionRules) NormalizedSkill
    }

    class DuplicateResolver {
        +resolve(normalized_skills: Sequence~NormalizedSkill~, rules: SkillExtractionRules) Sequence~NormalizedSkill~
        -_resolve_overlaps(skills: Sequence~NormalizedSkill~, rules: SkillExtractionRules) Sequence~NormalizedSkill~
        -_resolve_duplicates(skills: Sequence~NormalizedSkill~, rules: SkillExtractionRules) Sequence~NormalizedSkill~
    }

    class SkillEntityBuilder {
        +build(ns: NormalizedSkill, rules: SkillExtractionRules) ExtractedEntity
    }

    class SkillExtractionRules {
        +dictionary: Mapping
        +confidence_mappings: Mapping
        +extraction_scope: Sequence~str~
        +duplicate_strategy: str
        +overlap_strategy: str
        +default_confidence: float
    }

    class SkillCandidate {
        +matched_text: str
        +start_char: int
        +end_char: int
        +skill_id: str
        +match_type: str
        +match_term: str
        +segment_id: str
        +section_type: str
    }

    class NormalizedSkill {
        +candidate: SkillCandidate
        +skill_id: str
        +canonical_name: str
        +category: str
        +matched_token: str
        +normalized_token: str
        +dictionary_entry: str
        +alias_matched: str
        +synonym_matched: str
    }

    SkillExtractionService --> SkillExtractionPipeline : uses
    SkillExtractionPipeline --> SkillCandidateBuilder : uses
    SkillCandidateBuilder --> SkillMatcher : executes
    DictionaryMatcher ..|> SkillMatcher : implements
    SkillExtractionPipeline --> SkillCandidateValidator : uses
    SkillExtractionPipeline --> SkillNormalizer : uses
    SkillExtractionPipeline --> DuplicateResolver : uses
    SkillExtractionPipeline --> SkillEntityBuilder : uses
    SkillExtractionPipeline ..> SkillExtractionRules : consumes
    SkillNormalizer ..> NormalizedSkill : compiles
    SkillCandidateBuilder ..> SkillCandidate : compiles
    DuplicateResolver ..> NormalizedSkill : filters
```
