# Contact Information Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.2 — Contact Information Extraction  
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
                    subgraph contact
                        __init__.py
                        candidate_validator.py
                        contact_candidate.py
                        contact_rules.py
                        entity_builder.py
                        exceptions.py
                        extractor.py
                        normalizer.py
                        pattern_candidate_builder.py
                    end
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_contact_extraction.py
            end
        end
    end

    test_contact_extraction.py -.->|Tests| contact
```
