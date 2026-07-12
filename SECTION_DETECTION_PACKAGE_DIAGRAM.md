# Section Detection Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.3 — Document Section Detection  
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
                    subgraph section
                        __init__.py
                        exceptions.py
                        heading_validator.py
                        pipeline.py
                        section_boundary_resolver.py
                        section_builder.py
                        section_candidate_builder.py
                        section_models.py
                        section_rules.py
                        service.py
                    end
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_section_detection.py
            end
        end
    end

    test_section_detection.py -.->|Tests| section
```
