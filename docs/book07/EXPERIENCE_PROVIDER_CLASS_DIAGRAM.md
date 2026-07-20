# Experience Provider Class Diagram

```
┌──────────────────────────────────────────────┐
│        ExperienceRecommendationProvider      │
├──────────────────────────────────────────────┤
│ - _rules: ExperienceRecommendationRules      │
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
│ExpRules  │ │ExpBuild   │ │ExpValid   │ │ExpStats   │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + evalu- │ │ + build_  │ │ + validate│ │ + build() │
│   ate()  │ │   missing │ │   (recs)  │ └───────────┘
└──────────┘ │ + build_  │ └───────────┘
             │   partial │
             │ + build_  │
             │   duration│
             └───────────┘
```
