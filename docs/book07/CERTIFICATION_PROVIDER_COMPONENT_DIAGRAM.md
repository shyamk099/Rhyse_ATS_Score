# Certification Provider Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│            domain/recommendation/providers/                  │
│                                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ certification_provider.py│───►│ certification_rules.py  │  │
│  │ CertificationRecommendPr│    │ CertificationRecommendRu│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐    ┌─────────────────────────┐  │
│  │ certification_builder.py │    │ certification_validat...│  │
│  │ CertificationRecommendBl│    │ CertificationRecommendVa│  │
│  └────────────┬────────────┘    └─────────────────────────┘  │
│               │                                              │
│               ▼                                              │
│  ┌─────────────────────────┐                                 │
│  │ certification_stati...py│                                 │
│  │ CertificationRecommendSt│                                 │
│  └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────┘
```
