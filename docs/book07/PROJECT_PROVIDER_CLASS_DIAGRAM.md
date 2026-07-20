# Project Provider Class Diagram

```
┌──────────────────────────────────────────────┐
│          ProjectRecommendationProvider       │
├──────────────────────────────────────────────┤
│ - _rules: ProjectRecommendationRules         │
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
│ProjRules │ │ProjBuild  │ │ProjValid  │ │ProjStats  │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + evalu- │ │ + build_  │ │ + validate│ │ + build() │
│   ate()  │ │   missing │ │   (recs)  │ └───────────┘
└──────────┘ │ + build_  │ └───────────┘
             │   partial │
             │ + build_  │
             │   related │
             └───────────┘
```
