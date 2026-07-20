# Explainability Architecture

The Score Explainability Engine runs as a separate post-scoring reporting layer. It wraps `ScoreResult` inside a new immutable `ExplainabilityResult` DTO.

## Flow Architecture

```
Completed ScoreResult (overall_score = Optional float)
       │
       ▼
ExplainabilityEngine.explain()
       │
       ├──► Validation check
       │        └── Require 5 section scores present with valid raw/max scores
       │
       ├──► Section Score Explanation Generation
       │        ├── Calculate contribution: normalized_score * weight
       │        ├── ExplainabilityFormatter.format_section_formula()
       │        └── ExplainabilityFormatter.format_section_summary()
       │
       ├──► Overall Score Explanation Generation (Only if overall_score is not None)
       │        ├── ExplainabilityFormatter.format_overall_formula()
       │        └── ExplainabilityFormatter.format_overall_summary()
       │
       └──► Wrap into immutable ExplainabilityResult DTO
```
