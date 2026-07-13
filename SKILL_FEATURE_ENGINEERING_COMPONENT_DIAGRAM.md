# Skill Feature Engineering Component Diagram

## Book 04 — Feature Engineering | Milestone 4.2

The diagram maps the relationships of components within the Feature Extraction Layer:

```mermaid
graph TD
    subgraph "Service Boundary"
        Service["FeatureEngineeringService"]
    end

    subgraph "Skill Feature Component Context"
        Extractor["SkillFeatureExtractor"]
        Validator["SkillFeatureValidator"]
        Normalizer["SkillFeatureNormalizer"]
        Builder["SkillFeatureBuilder"]
        Stats["SkillFeatureStatisticsBuilder"]
    end

    subgraph "Core Pipeline Infrastructure"
        Pipeline["FeatureEngineeringPipeline"]
    end

    Service --> Pipeline
    Pipeline --> Extractor
    Extractor --> Validator
    Extractor --> Normalizer
    Extractor --> Builder
    Extractor --> Stats
```
