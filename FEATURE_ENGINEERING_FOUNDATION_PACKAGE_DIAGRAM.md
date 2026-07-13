# Feature Engineering Foundation Package Diagram

## Book 04 — Feature Engineering | Milestone 4.1

The package boundaries mapping illustrates the logical sub-folders and class distributions in Book 04:

```mermaid
graph TD
    subgraph domain.feature_engineering ["ats_engine.domain.feature_engineering"]
        Models["models.py<br/>(Immutable DTOs)"]
        Extractor["extractor.py<br/>(Abstract interface)"]
        Registry["registry.py<br/>(Class registry)"]
        Factory["factory.py<br/>(Instance factory)"]
        Pipeline["pipeline.py<br/>(Executor pipeline)"]
        Service["service.py<br/>(FeatureEngineeringService)"]
        Exceptions["exceptions.py<br/>(Typed Exception classes)"]
    end

    subgraph domain.entity_extraction.canonical ["ats_engine.domain.entity_extraction.canonical"]
        CanonicalModels["canonical_models.py<br/>(CanonicalEntityCollection)"]
    end

    Service --> Models
    Service --> Extractor
    Service --> Registry
    Service --> Factory
    Service --> Pipeline
    Service --> Exceptions

    Pipeline --> Extractor
    Pipeline --> Models
    Pipeline --> Exceptions

    Factory --> Registry
    Factory --> Extractor
    Factory --> Exceptions

    Registry --> Extractor
    Registry --> Exceptions

    Extractor --> Models
    Extractor --> CanonicalModels
```
