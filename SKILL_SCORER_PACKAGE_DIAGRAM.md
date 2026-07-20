# Skill Scorer Package Diagram

```mermaid
graph TD
    subgraph Package: ats_scoring.skill
        __init__.py[__init__.py]
        scorer.py[scorer.py]
        resolver.py[resolver.py]
        rules.py[rules.py]
        validator.py[validator.py]
        breakdown_builder.py[breakdown_builder.py]
        statistics_builder.py[statistics_builder.py]
    end

    subgraph Dependency: ats_scoring core
        exceptions.py[ats_scoring.exceptions]
        models.py[ats_scoring.models]
    end

    __init__.py --> scorer.py & resolver.py & rules.py & validator.py
    scorer.py --> resolver.py & rules.py & validator.py & breakdown_builder.py & statistics_builder.py
    validator.py --> exceptions.py
    breakdown_builder.py & scorer.py --> models.py
```
