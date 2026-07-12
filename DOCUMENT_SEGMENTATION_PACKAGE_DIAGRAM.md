# Document Segmentation Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.3 — Document Segmentation & Reading Order  
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
                    reading_order.py
                    segment_builder.py
                    segment_validator.py
                    segmentation_models.py
                    segmentation_rules.py
                    segmenter.py
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_document_segmentation.py
            end
        end
    end

    test_document_segmentation.py -.->|Tests| segmenter.py
```
