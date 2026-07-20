# Project Scorer Dependency Graph

```mermaid
graph TD
    subgraph Layer: Project Scorer Package
        ats_scoring/project/scorer.py --> ats_scoring/project/resolver.py
        ats_scoring/project/scorer.py --> ats_scoring/project/rules.py
        ats_scoring/project/scorer.py --> ats_scoring/project/validator.py
        ats_scoring/project/scorer.py --> ats_scoring/project/breakdown_builder.py
        ats_scoring/project/scorer.py --> ats_scoring/project/statistics_builder.py
    end

    subgraph Dependency: ats_scoring Core DTOs and Interfaces
        ats_scoring/exceptions.py --> ats_scoring/project/validator.py
        ats_scoring/interfaces.py --> ats_scoring/project/scorer.py
        ats_scoring/interfaces.py --> ats_scoring/project/resolver.py
        ats_scoring/models/score_breakdown.py & ats_scoring/models/section_score.py --> ats_scoring/project/scorer.py
    end

    subgraph Dependency: Book 05 Output DTO
        matching/models.py[ats_engine.domain.matching.models]
    end

    ats_scoring/project/resolver.py & ats_scoring/project/validator.py & ats_scoring/project/breakdown_builder.py --> matching/models.py
```
