# Feature Engineering Foundation Sequence Diagram

## Book 04 — Feature Engineering | Milestone 4.1

The sequence diagram below displays the execution timeline for extracting features via the pipeline:

```mermaid
sequenceDiagram
    autonumber
    actor Caller
    participant Service as FeatureEngineeringService
    participant Registry as FeatureExtractorRegistry
    participant Factory as FeatureExtractorFactory
    participant Pipeline as FeatureEngineeringPipeline
    participant Extractor as FeatureExtractor

    Caller ->> Service: extract_features(entities, enabled_extractors, rules)
    Note over Service: Construct FeatureExtractionContext
    
    loop For each enabled extractor key
        Service ->> Factory: get_extractor(key)
        Factory ->> Registry: get(key)
        Registry -->> Factory: ExtractorClass
        Note over Factory: Instantiate class dynamically
        Factory -->> Service: extractor_instance
    end

    Service ->> Pipeline: execute(entities, extractors, context)
    
    loop For each extractor instance
        Pipeline ->> Extractor: extract(entities, context)
        Extractor -->> Pipeline: Sequence[Feature]
        Note over Pipeline: Append features & update stats
    end
    
    Note over Pipeline: Compute total execution duration
    Pipeline -->> Service: FeatureCollection
    Service -->> Caller: FeatureCollection
```
