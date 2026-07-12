# Skill Extraction Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.4 — Skill Extraction  
**Status:** COMPLETE  

---

# Purpose

This document contains the package diagram detailing the directory structure.

---

# Package Layout

```mermaid
flowchart TD
    subgraph src [src/ package root]
        subgraph ats_engine
            subgraph domain
                subgraph entity_extraction
                    subgraph skills
                        __init__.py
                        exceptions.py
                        matcher.py
                        duplicate_resolver.py
                        pipeline.py
                        skill_candidate_builder.py
                        skill_candidate_validator.py
                        skill_entity_builder.py
                        skill_models.py
                        skill_rules.py
                        service.py
                    end
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_skill_extraction.py
            end
        end
    end

    test_skill_extraction.py -.->|Tests| skills
```
