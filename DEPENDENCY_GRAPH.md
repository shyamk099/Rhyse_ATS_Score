# Dependency Graph

```mermaid
flowchart TD
    subgraph Composition [ats_engine.application]
        CR[CompositionRoot]
    end

    subgraph Config [ats_engine.infrastructure.configuration]
        CS[ConfigurationService]
        AM[ApplicationSettings]
    end

    subgraph Logging [ats_engine.infrastructure.logging]
        LS[LoggingService]
        LF[LoggerFactory]
    end

    subgraph Rules [ats_engine.domain.rule_engine]
        RES[RuleEngineService]
    end

    %% Dependency Direction
    CR --> CS
    CR --> RES
    CR --> AM
    CR ..> LS

    RES --> LF
    CS --> AM
```
