# Experience Feature Engineering Component Diagram

## Book 04 — Feature Engineering | Milestone 4.3

The diagram maps the relationships of components within the Feature Extraction Layer:

```mermaid
graph TD
    subgraph "Service Boundary"
        Service["FeatureEngineeringService"]
    end

    subgraph "Experience Feature Component Context"
        Extractor["ExperienceFeatureExtractor"]
        Validator["ExperienceFeatureValidator"]
        Normalizer["ExperienceFeatureNormalizer"]
        Builder["ExperienceFeatureBuilder"]
        Stats["ExperienceFeatureStatisticsBuilder"]
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
