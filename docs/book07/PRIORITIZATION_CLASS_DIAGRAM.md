# Prioritization Class Diagram

```
┌──────────────────────────────────────────────┐
│             PrioritizationEngine             │
├──────────────────────────────────────────────┤
│ - _rules: PrioritizationRules                │
├──────────────────────────────────────────────┤
│ + process(result) → PrioritizedResult        │
└──────────────────────────────────────────────┘
    │           │               │            │
    ▼           ▼               ▼            ▼
┌──────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ProjRules │ │ProjBuild  │ │ProjValid  │ │ProjStats  │
├──────────┤ ├───────────┤ ├───────────┤ ├───────────┤
│ + resolve│ │ + priorit-│ │ + validate│ │ + build() │
│   profile│ │   ize_sort│ └───────────┘ └───────────┘
└──────────┘ └───────────┘
```
