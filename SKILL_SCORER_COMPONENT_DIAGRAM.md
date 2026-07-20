# Skill Scorer Component Diagram

```mermaid
graph TD
    subgraph Component: SkillScorer Module
        Scorer[SkillScorer]
        Resolver[SkillClassificationResolver]
        Validator[SkillScoreValidator]
        BreakdownBuilder[SkillBreakdownBuilder]
        StatsBuilder[SkillStatisticsBuilder]
    end

    subgraph Inputs
        Context[ScoringContext]
        Results[Skill MatchResult tuple]
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
