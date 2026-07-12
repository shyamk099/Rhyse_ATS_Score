# ATS Resume Intelligence Engine — Traceability Matrix

## Legend

`TBD` means the handbook requires an artifact but does not supply or name it; it is not an implementation recommendation. Logical module/class/interface labels describe ownership boundaries, not implemented code. All entries depend on immutable version metadata and validated Rule JSON where applicable.

| Handbook chapter | Folder/package | Logical classes/interfaces | Rule files | Tests | Dependencies |
|---|---|---|---|---|---|
| `README.md` | repository | documentation entry point | — | doc-link check | docs |
| `docs/ats_resume_only_score_engine.md` | resume-only scoring | resume-only orchestrator; component score/advisory interfaces | Resume-only scoring rules TBD | score/advisory/calibration regression | Resume input, embeddings, benchmark TBD |
| `Resume+JD/README.md` | handbook root | documentation entry point | — | doc-link check | handbook |
| `00_Overview/Project_Overview.md` | architecture governance | system scope/version policy | all categories | architecture conformance | Books 01–09 |
| `00_Overview/Product_Vision.md` | architecture governance | product-policy boundary | — | requirements traceability | Project Overview |
| `00_Overview/Architecture_Decisions.md` | architecture governance | ADR compliance boundary | all categories | deterministic/immutability checks | all engines |
| `00_Overview/System_Glossary.md` | shared contracts | terminology/contract registry | — | terminology validation | all books |
| `00_Overview/Version_History.md` | versioning | version registry | version metadata | compatibility tests | all versioned outputs |
| `01_System_Architecture/Book_01_System_Architecture.md` | composition/architecture | layer/engine ports | all categories | dependency-direction tests | Book 00 |
| `01_System_Architecture/Core_Design_Principles.md` | composition/architecture | policy guards | all categories | ADR conformance | Book 00 |
| `01_System_Architecture/Architecture_Diagrams.md` | architecture documentation | pipeline contracts | — | diagram/doc check | Books 02–09 |
| `02_Document_Processing/Book_02_Document_Parser.md` | `document_processing` | ingestion pipeline | parser | integration tests | file input/rules |
| `02_Document_Processing/Text_Extraction.md` | `document_processing` | text extractor | parser | extraction fixtures | files/OCR |
| `02_Document_Processing/OCR.md` | `document_processing` | OCR detector/processor | parser | OCR confidence tests | OCR provider TBD |
| `02_Document_Processing/Resume_Parser.md` | `document_processing` | Resume parser | parser | Resume parser fixtures | Text Object/rules |
| `02_Document_Processing/JD_Parser.md` | `document_processing` | JD parser | parser | JD parser fixtures | Text Object/rules |
| `02_Document_Processing/JSON_Schemas.md` | `contracts` | Resume/JD/entity/feature/evidence/score/API validators | schema metadata | schema compatibility | Books 03–09 |
| `03_Entity_Extraction/Book_03_Entity_Extraction.md` | `entity_extraction` | extraction pipeline | entity | integration tests | parsed JSON |
| `03_Entity_Extraction/Resume_Entities.md` | `entity_extraction` | Resume entity extractor | entity | per-type/source tests | Resume JSON |
| `03_Entity_Extraction/JD_Entities.md` | `entity_extraction` | JD entity extractor | entity | per-type/source tests | JD JSON |
| `03_Entity_Extraction/Entity_Normalization.md` | `entity_extraction` | normalizer | entity | preservation/normalization tests | aliases/ontology TBD |
| `03_Entity_Extraction/Entity_Relationships.md` | `entity_extraction` | relationship builder | entity | relationship tests | entities |
| `03_Entity_Extraction/Entity_Confidence.md` | `entity_extraction` | confidence calculator | entity | boundary tests | extraction/normalization |
| `03_Entity_Extraction/Entity_JSON_Specification.md` | `contracts` | Entity JSON validator | schema metadata | contract tests | entity output |
| `04_Feature_Engineering/Book_04_Feature_Engineering.md` | `feature_engineering` | feature pipeline | feature | integration tests | Entity JSON |
| `04_Feature_Engineering/Resume_Feature_Engineering.md` | `feature_engineering` | Resume feature calculator | feature | calculation fixtures | Resume entities |
| `04_Feature_Engineering/JD_Feature_Engineering.md` | `feature_engineering` | JD feature calculator | feature | calculation fixtures | JD entities |
| `04_Feature_Engineering/Derived_Features.md` | `feature_engineering` | derived feature calculator | feature | dependency tests | primitive features |
| `04_Feature_Engineering/Feature_Calculation.md` | `feature_engineering` | calculation service | feature | formula/boundary tests | entities/rules |
| `04_Feature_Engineering/Feature_Confidence.md` | `feature_engineering` | confidence calculator | feature | confidence tests | feature sources |
| `04_Feature_Engineering/Feature_JSON_Specification.md` | `contracts` | Feature JSON validator | schema metadata | contract tests | feature output |
| `05_Hybrid_Knowledge_Layer/Book_05_Hybrid_Knowledge_Layer.md` | `knowledge_matching` | matching orchestrator | matching | pipeline tests | Feature JSON |
| `05_Hybrid_Knowledge_Layer/Exact_Matching.md` | `knowledge_matching` | exact strategy | matching | exact tests | canonical values |
| `05_Hybrid_Knowledge_Layer/Alias_Dictionary.md` | knowledge assets | alias dictionary provider | entity/matching | alias data tests | dictionary TBD |
| `05_Hybrid_Knowledge_Layer/Alias_Matching.md` | `knowledge_matching` | alias strategy | matching | alias tests | dictionary |
| `05_Hybrid_Knowledge_Layer/Fuzzy_Matching.md` | `knowledge_matching` | fuzzy strategy | matching | threshold tests | matching rules |
| `05_Hybrid_Knowledge_Layer/Technology_Ontology.md` | knowledge assets | ontology provider | entity/matching | ontology integrity tests | ontology TBD |
| `05_Hybrid_Knowledge_Layer/Ontology_Matching.md` | `knowledge_matching` | ontology strategy | matching | traversal tests | ontology |
| `05_Hybrid_Knowledge_Layer/Semantic_Matching.md` | `knowledge_matching` | semantic strategy/embedding port | matching | deterministic adapter tests | embedding provider TBD |
| `05_Hybrid_Knowledge_Layer/Matching_Pipeline.md` | `knowledge_matching` | strategy pipeline | matching | precedence tests | all strategies |
| `05_Hybrid_Knowledge_Layer/Matching_Confidence.md` | `knowledge_matching` | match confidence calculator | matching | confidence tests | match/feature confidence |
| `05_Hybrid_Knowledge_Layer/Match_JSON_Specification.md` | `contracts` | Match JSON validator | schema metadata | contract tests | Feature JSON |
| `06_Evidence_Intelligence/Book_06_Evidence_Intelligence.md` | `evidence_intelligence` | evidence pipeline | evidence | integration tests | Match JSON |
| `06_Evidence_Intelligence/Evidence_Generation.md` | `evidence_intelligence` | generator | evidence | evidence fixture tests | matches |
| `06_Evidence_Intelligence/Requirement_Evidence.md` | `evidence_intelligence` | requirement builder | evidence | status/coverage tests | JD requirements/matches |
| `06_Evidence_Intelligence/Section_Evidence.md` | `evidence_intelligence` | section builder | evidence | section tests | Resume/matches |
| `06_Evidence_Intelligence/Evidence_Validation.md` | `evidence_intelligence` | validator | evidence | broken-reference tests | evidence objects |
| `06_Evidence_Intelligence/Evidence_Confidence.md` | `evidence_intelligence` | confidence calculator | evidence | boundary tests | evidence/matches |
| `06_Evidence_Intelligence/Evidence_Aggregation.md` | `evidence_intelligence` | aggregator | evidence | aggregation tests | validated evidence |
| `06_Evidence_Intelligence/Explainability_Model.md` | `evidence_intelligence` | explanation builder | evidence | traceability tests | evidence/coverage |
| `06_Evidence_Intelligence/Evidence_JSON_Specification.md` | `contracts` | Evidence JSON validator | schema metadata | contract tests | Match JSON |
| `07_ATS_Scoring/Book_07_ATS_Scoring.md` | `ats_scoring` | score orchestrator | scoring | end-to-end score tests | Evidence JSON |
| `07_ATS_Scoring/ATS_Compatibility.md` | `ats_scoring` | compatibility calculator | scoring | component tests | parsed Resume/evidence |
| `07_ATS_Scoring/Resume_Quality.md` | `ats_scoring` | shared quality calculator | scoring | shared-mode tests | features/evidence |
| `07_ATS_Scoring/Resume_JD_Matching.md` | `ats_scoring` | match-score calculator | scoring | coverage/weight tests | Evidence JSON |
| `07_ATS_Scoring/Semantic_Validation_Score.md` | `ats_scoring` | semantic-validation calculator | scoring | evidence tests | Evidence JSON |
| `07_ATS_Scoring/Integrity_Penalty.md` | `ats_scoring` | integrity validator/calculator | scoring | violation/cap tests | Resume/evidence/rules |
| `07_ATS_Scoring/Weighted_Scoring_Engine.md` | `ats_scoring` | weighted scorer | scoring | formula/100%-weight tests | components/penalty |
| `07_ATS_Scoring/Score_Calibration.md` | `ats_scoring` | calibrator | scoring | calibration regression | dataset/spec TBD |
| `07_ATS_Scoring/Score_Versioning.md` | `ats_scoring` | version manager | scoring | reproducibility tests | all versions |
| `07_ATS_Scoring/ATS_Final_Score.md` | `ats_scoring` | score publisher | scoring | bounds/classification tests | raw/calibrated score |
| `07_ATS_Scoring/Score_JSON_Specification.md` | `contracts` | Score JSON validator | schema metadata | contract tests | Evidence/score |
| `08_ATS_Recommendation_Engine/Book_08_ATS_Recommendation_Engine.md` | `recommendations` | recommendation orchestrator | recommendation | integration tests | Evidence/Score JSON |
| `08_ATS_Recommendation_Engine/01_Gap_Analysis.md` | `recommendations` | gap analyzer | recommendation | gap tests | evidence/score |
| `08_ATS_Recommendation_Engine/02_Recommendation_Generation.md` | `recommendations` | generator | recommendation | evidence/truthfulness tests | gaps |
| `08_ATS_Recommendation_Engine/03_Recommendation_Prioritization.md` | `recommendations` | prioritizer | recommendation | priority tests | recommendations/impact |
| `08_ATS_Recommendation_Engine/04_Score_Impact_Estimation.md` | `recommendations` | impact estimator | recommendation | range/confidence tests | gaps/scores |
| `08_ATS_Recommendation_Engine/05_Recommendation_Validation.md` | `recommendations` | validator | recommendation | technical/business/ethical tests | recommendations/evidence |
| `08_ATS_Recommendation_Engine/06_Recommendation_JSON_Specification.md` | `contracts` | Recommendation JSON validator | schema metadata | contract tests | recommendations |
| `08_ATS_Recommendation_Engine/07_Recommendation_API_Contract.md` | API adapter | API controller/report repository | API config TBD | endpoint/status/security tests | recommendations, auth/store TBD |
| `09_ATS_Rule_Engine/Book_09_ATS_Rule_Engine.md` | `rule_engine` | rule lifecycle services | Rule JSON | activation tests | rule assets TBD |
| `09_ATS_Rule_Engine/01_Parsing_Rules.md` | `rule_engine` | parser rule provider | parser | rule validation | parser config TBD |
| `09_ATS_Rule_Engine/02_Entity_Rules.md` | `rule_engine` | entity rule provider | entity | rule validation | entity config TBD |
| `09_ATS_Rule_Engine/03_Feature_Rules.md` | `rule_engine` | feature rule provider | feature | rule validation | feature config TBD |
| `09_ATS_Rule_Engine/04_Matching_Rules.md` | `rule_engine` | matching rule provider | matching | precedence/threshold tests | matching config TBD |
| `09_ATS_Rule_Engine/05_Evidence_Rules.md` | `rule_engine` | evidence rule provider | evidence | rule validation | evidence config TBD |
| `09_ATS_Rule_Engine/06_Scoring_Rules.md` | `rule_engine` | scoring rule provider | scoring | weights/penalty tests | scoring config TBD |
| `09_ATS_Rule_Engine/07_Recommendation_Rules.md` | `rule_engine` | recommendation rule provider | recommendation | rule validation | recommendation config TBD |
| `09_ATS_Rule_Engine/08_Rule_JSON_Specification.md` | `contracts`/`rule_engine` | loader/schema/version validator | Rule JSON | complete/invalid set tests | all rule categories |

## Unmapped required artifacts / OPEN QUESTIONS

Every Markdown handbook chapter is mapped above. The following required artifacts remain absent from the repository and therefore cannot be mapped to concrete files: activated Rule JSON/YAML files; alias dictionary; technology ontology; calibration/benchmark datasets; document/parser/OCR fixtures; semantic model assets; tests; API/auth/rate-limit configuration; and evaluation/report persistence. Their authority and locations must be supplied before implementation.
