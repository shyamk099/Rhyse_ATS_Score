# Experience Scorer Component Diagram

```mermaid
graph TD
    subgraph Component: ExperienceScorer Module
        Scorer[ExperienceScorer]
        Resolver[ExperienceClassificationResolver]
        Validator[ExperienceScoreValidator]
        BreakdownBuilder[ExperienceBreakdownBuilder]
        StatsBuilder[ExperienceStatisticsBuilder]
    end

    subgraph Inputs
        Context[ScoringContext]
        Results[Experience MatchResult tuple]
    end

    subgraph Outputs
        Breakdown[ScoreBreakdown DTO]
        SecScore[SectionScore DTO]
    end

    Context --> Scorer
    Results --> Validator
    Scorer --> Validator
    Scorer --> Resolver
    Scorer --> BreakdownBuilder
    Scorer --> StatsBuilder
    BreakdownBuilder --> Breakdown
    Breakdown --> SecScore
```
