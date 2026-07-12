# Structural Analysis Package Diagram

**Version:** 1.0  
**Author:** Principal Software Engineer  
**Generated Date:** 2026-07-12  
**Related Handbook Chapter:** Book 02 — Document Processing  
**Related Milestone:** Milestone 2.2 — Resume & JD Structural Analysis  
**Status:** COMPLETE  

---

# Purpose

This document details the package diagram for the structural analyzer layer.

---

# Package Layout

```mermaid
flowchart TD
    subgraph src [src/ package root]
        subgraph ats_engine
            subgraph domain
                subgraph document_processing
                    structural_analyzer.py
                    structural_rules.py
                    structure_models.py
                end
            end
        end
    end

    subgraph tests
        subgraph unit
            subgraph domain_tests [domain package tests]
                test_structural_analysis.py
            end
        end
    end

    test_structural_analysis.py -.->|Tests| structural_analyzer.py
```
