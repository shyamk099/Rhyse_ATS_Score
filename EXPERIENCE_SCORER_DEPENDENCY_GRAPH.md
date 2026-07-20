# Experience Scorer Dependency Graph

```mermaid
graph TD
    subgraph Layer: Experience Scorer Package
        ats_scoring/experience/scorer.py --> ats_scoring/experience/resolver.py
        ats_scoring/experience/scorer.py --> ats_scoring/experience/rules.py
        ats_scoring/experience/scorer.py --> ats_scoring/experience/validator.py
        ats_scoring/experience/scorer.py --> ats_scoring/experience/breakdown_builder.py
        ats_scoring/experience/scorer.py --> ats_scoring/experience/statistics_builder.py
    end

    subgraph Dependency: ats_scoring Core DTOs and Interfaces
        ats_scoring/exceptions.py --> ats_scoring/experience/validator.py
        ats_scoring/interfaces.py --> ats_scoring/experience/scorer.py
        ats_scoring/models/score_breakdown.py & ats_scoring/models/section_score.py --> ats_scoring/experience/scorer.py
    end

    subgraph Dependency: Book 05 Output DTO
        matching/models.py[ats_engine.domain.matching.models]
    end

    ats_scoring/experience/resolver.py & ats_scoring/experience/validator.py & ats_scoring/experience/breakdown_builder.py --> matching/models.py
```
