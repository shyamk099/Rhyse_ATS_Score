# Skill Scorer Dependency Graph

```mermaid
graph TD
    subgraph Layer: Skill Scorer Package
        ats_scoring/skill/scorer.py --> ats_scoring/skill/resolver.py
        ats_scoring/skill/scorer.py --> ats_scoring/skill/rules.py
        ats_scoring/skill/scorer.py --> ats_scoring/skill/validator.py
        ats_scoring/skill/scorer.py --> ats_scoring/skill/breakdown_builder.py
        ats_scoring/skill/scorer.py --> ats_scoring/skill/statistics_builder.py
    end

    subgraph Dependency: ats_scoring Core DTOs
        ats_scoring/exceptions.py --> ats_scoring/skill/validator.py
        ats_scoring/models/score_breakdown.py & ats_scoring/models/section_score.py --> ats_scoring/skill/scorer.py
    end

    subgraph Dependency: Book 05 Output DTO
        matching/models.py[ats_engine.domain.matching.models]
    end

    ats_scoring/skill/resolver.py & ats_scoring/skill/validator.py & ats_scoring/skill/breakdown_builder.py --> matching/models.py
```
