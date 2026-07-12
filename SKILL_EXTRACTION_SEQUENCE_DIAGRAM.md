# Skill Extraction Sequence Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.4 — Skill Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the sequence diagram representing skill extraction.

---

# Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant SES as SkillExtractionService
    participant SEP as SkillExtractionPipeline
    participant SCB as SkillCandidateBuilder
    participant DM as DictionaryMatcher
    participant SCV as SkillCandidateValidator
    participant SN as SkillNormalizer
    participant DR as DuplicateResolver
    participant SEB as SkillEntityBuilder

    Client->>SES: extract_skills(doc, sections, config)
    SES->>SEP: execute(doc, sections, rules)
    
    SEP->>SCB: build_candidates(doc, sections, rules)
    loop For each permitted section
        loop For each segment in section
            SCB->>DM: match(segment, rules, section_type)
            DM-->>SCB: list[SkillCandidate]
        end
    end
    SCB-->>SEP: raw_candidates list
    
    loop For each candidate in raw_candidates
        SEP->>SCV: validate(candidate, rules)
        alt is valid
            SEP->>SN: normalize(candidate, rules)
            SN-->>SEP: NormalizedSkill DTO
        end
    end
    
    SEP->>DR: resolve(normalized_list, rules)
    DR->>DR: Check overlap spans (longest wins)
    DR->>DR: Apply duplicate strategies
    DR-->>SEP: resolved_normalized list (Filtered)
    
    loop For each item in resolved_normalized
        SEP->>SEB: build(ns, rules)
        SEB->>SEB: Map domain ExtractedEntity offsets & reasons
        SEB-->>SEP: ExtractedEntity
    end
    
    SEP-->>SES: SkillCollection
    SES-->>Client: SkillCollection
```
