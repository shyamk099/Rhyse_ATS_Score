# Common Feature Engineering Utilities Design Document

## Book 04 — Feature Engineering | Shared Context

### Purpose

This document details the reusable shared utilities implemented under `common/` for validation, normalization, provenance compiling, and custom object mapping.

---

### Component Schema

```
common/
   ├── normalization.py (normalize_text - collapses whitespace and trims margins)
   ├── validation.py    (validate_required_fields / validate_confidence_threshold)
   ├── provenance.py    (build_provenance - wraps FeatureProvenance builder logic)
   └── url_mapping.py   (map_custom_url - maps ProjectURL/CertificationURL to dict)
```

---

### Key Helpers

1. **`normalize_text`**:
   Accepts `str | None` and returns a trimmed, whitespace-collapsed string or `None`.
2. **`validate_required_fields`**:
   Inspects default name/value and metadata dictionary values against rule configs.
3. **`validate_confidence_threshold`**:
   Ensures score exceeds lower bounds.
4. **`build_provenance`**:
   Extracts identifier and segment context fields.
5. **`map_custom_url`**:
   Safely extracts original/normalized URL components.
