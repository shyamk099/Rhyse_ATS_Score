# Document Processing Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.1 — Document Processing Foundation  
**Status:** COMPLETE  

---

# Purpose

This document contains the package diagram demonstrating the directory structure.

---

# Package Layout

```mermaid
flowchart TD
    subgraph src [src/ package root]
        subgraph ats_engine
            subgraph domain
                subgraph document_processing
                    __init__.py
                    docx_parser.py
                    exceptions.py
                    factory.py
                    models.py
                    normalization.py
                    parser.py
                    pdf_parser.py
                    registry.py
                    service.py
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_document_processing.py
            end
        end
    end

    test_document_processing.py -.->|Verifies| document_processing
```
