# Canonical Document Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.4 — Canonical Document Validation  
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
                subgraph document_processing
                    canonical_assembler.py
                    canonical_builder.py
                    canonical_models.py
                    canonical_rules.py
                    consistency_validator.py
                    integrity_validator.py
                    statistics_builder.py
                    validation_service.py
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_canonical_validation.py
            end
        end
    end

    test_canonical_validation.py -.->|Tests| validation_service.py
```
