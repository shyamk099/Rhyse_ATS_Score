# Entity Extraction Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 03 — Entity Extraction  
**Related Milestone:** Milestone 3.1 — Entity Extraction Foundation  
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
                    __init__.py
                    exceptions.py
                    extractor.py
                    factory.py
                    models.py
                    pipeline.py
                    registry.py
                    service.py
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_entity_extraction.py
            end
        end
    end

    test_entity_extraction.py -.->|Tests| entity_extraction
```
