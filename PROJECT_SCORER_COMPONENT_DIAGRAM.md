# Project Scorer Component Diagram

```mermaid
graph TD
    subgraph Component: ProjectScorer Module
        Scorer[ProjectScorer]
        Resolver[ProjectClassificationResolver]
        Validator[ProjectScoreValidator]
        BreakdownBuilder[ProjectBreakdownBuilder]
        StatsBuilder[ProjectStatisticsBuilder]
    end

    subgraph Inputs
        Context[ScoringContext]
        Results[Project MatchResult tuple]
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
