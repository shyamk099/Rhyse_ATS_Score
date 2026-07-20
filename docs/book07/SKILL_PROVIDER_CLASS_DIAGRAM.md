# Skill Provider Class Diagram

```
┌──────────────────────────────────────────────┐
│          SkillRecommendationProvider         │
├──────────────────────────────────────────────┤
│ - _rules: SkillRecommendationRules           │
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
│SkillRules│ │SkillBuild │ │SkillValid │ │SkillStats │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + should_│ │ + build_  │ │ + validate│ │ + build() │
│   recomm.│ │   missing │ │   (recs)  │ └───────────┘
└──────────┘ │ + build_  │ └───────────┘
             │   partial │
             └───────────┘
```
