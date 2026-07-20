# Explainability Class Diagram

```
┌──────────────────────────────────────────────┐
│             ExplainabilityEngine             │
├──────────────────────────────────────────────┤
│ - _weight_config: SectionWeightConfiguration │
│ - _logger: Logger                            │
├──────────────────────────────────────────────┤
│ + explain(ScoreResult) → ExplainabilityResult│
│ + weight_config: SectionWeightConfiguration  │
└──────────────────────────────────────────────┘
           │ uses                    │ uses
           ▼                         ▼
┌─────────────────────┐   ┌─────────────────────────────┐
│ExplainabilityForm...│   │ ExplainabilityResult (DTO)  │
├─────────────────────┤   ├─────────────────────────────┤
│ + format_section... │   │ + score_result: ScoreResult │
│ + format_section... │   │ + overall_explanation: ...  │
│ + format_overall... │   │ + section_explanations: ... │
│ + format_overall... │   │ + statistics: dict          │
└─────────────────────┘   │ + metadata: dict            │
                          └─────────────────────────────┘
                                     │ contains
                                     ▼
                      ┌──────────────────────────────┐
                      │    OverallExplanation        │
                      ├──────────────────────────────┤
                      │ + overall_score: float       │
                      │ + formula: str               │
                      │ + section_contributions: dict│
                      │ + summary: str               │
                      └──────────────────────────────┘
                                     │ contains
                                     ▼
                      ┌──────────────────────────────┐
                      │    SectionExplanation        │
                      ├──────────────────────────────┤
                      │ + section_name: str          │
                      │ + raw_score: float           │
                      │ + normalized_score: float    │
                      │ + matched_items: tuple       │
                      │ + missing_items: tuple       │
                      │ + formula: str               │
                      │ + summary: str               │
                      └──────────────────────────────┘

Exception Hierarchy:
  ScoringError
    └── ExplainabilityError
          ├── FormattingError
          └── ExplainabilityValidationError
```
