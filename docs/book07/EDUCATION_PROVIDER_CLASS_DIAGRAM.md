# Education Provider Class Diagram

```
┌──────────────────────────────────────────────┐
│         EducationRecommendationProvider      │
├──────────────────────────────────────────────┤
│ - _rules: EducationRecommendationRules       │
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
│EduRules  │ │EduBuild   │ │EduValid   │ │EduStats   │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + evalu- │ │ + build_  │ │ + validate│ │ + build() │
│   ate()  │ │   missing │ │   (recs)  │ └───────────┘
└──────────┘ │ + build_  │ └───────────┘
             │   partial │
             │ + build_  │
             │   levelgap│
             └───────────┘
```
