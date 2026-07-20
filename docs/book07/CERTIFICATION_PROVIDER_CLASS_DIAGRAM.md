# Certification Provider Class Diagram

```
┌──────────────────────────────────────────────┐
│       CertificationRecommendationProvider    │
├──────────────────────────────────────────────┤
│ - _rules: CertificationRecommendationRules   │
│ - _last_statistics: dict                     │
├──────────────────────────────────────────────┤
│ + generate(context) → tuple[Recommendation]  │
│ + validate(context)                          │
│ + last_statistics: dict                      │
└──────────────────────────────────────────────┘
    │          │               │             │
    │ uses     │ uses          │ uses        │ uses
    ▼          ▼               ▼             ▼
┌──────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│CertRules │ │CertBuild  │ │CertValid  │ │CertStats  │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + evalu- │ │ + build_  │ │ + validate│ │ + build() │
│   ate()  │ │   missing │ │   (recs)  │ └───────────┘
└──────────┘ │ + build_  │ └───────────┘
             │   partial │
             │ + build_  │
             │   expired │
             └───────────┘
```
