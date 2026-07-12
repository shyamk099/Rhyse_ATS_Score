# Architecture Documentation Review Report

## Verdict

The documents are not yet ready for coding. They preserve the handbook's intent and contain all repository Markdown chapters in the traceability matrix, but several blocking specification and architecture-boundary issues remain. No business logic has been modified by this review.

## Review scope

Reviewed: `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, and `TRACEABILITY_MATRIX.md` against the supplied handbook, including its canonical-contract, layering, deterministic-scoring, and rule-engine requirements.

## Findings

| ID | Severity | Area | Finding | Evidence / impact |
|---|---|---|---|---|
| R-02 | Blocker | Business-logic authority | Matching priority remains unresolved. The architecture adopts Exact → Alias → Fuzzy → Ontology → Semantic, but Rule JSON supplies Exact → Alias → Ontology → Fuzzy → Semantic. | This changes which strategy owns a match and therefore its confidence, reason, and downstream evidence. Coding either order before an authority decision would create business-logic drift. |
| R-03 | High | Layering / Clean Architecture | The architecture states that layers communicate only with adjacent layers, while its component diagram shows Rule JSON directly feeding Processing, Intelligence, Scoring, and Recommendation. | The diagram either violates the declared rule or needs an explicit startup/composition exception. Rule activation/configuration injection is cross-cutting; it must be distinguished from runtime business-data flow before implementation. |
| R-04 | High | Scoring dependencies | The traceability matrix says ATS Compatibility depends on “parsed Resume/evidence” and Integrity Penalty depends on “Resume/evidence/rules,” while Book 07 states the scoring engine consumes validated Evidence JSON and never performs parsing. | This creates a direct Scoring → Processing dependency that skips the Intelligence layer and conflicts with the score-engine input contract. The handbook must establish whether these components are upstream evidence producers or whether the necessary facts are carried in Evidence JSON. |
| R-05 | High | Missing interface / layer | The required Output Engine and Confidence Aggregator are incomplete in the architecture and absent as planned milestones. | Book 01 assigns both to the Output Layer. `ARCHITECTURE.md` lists output consumption of confidence but does not define a confidence-aggregator interface, inputs, output model, orchestration step, or test scope. The sequence has no confidence-aggregation call. |
| R-07 | High | Required artifacts | Rule JSON, alias dictionary, technology ontology, activated configuration, benchmark/calibration inputs, fixtures, and tests are referenced but absent. | The documents correctly mark these as TBD; however, they are mandatory operational dependencies, not optional implementation details. Their absence blocks deterministic, reproducible implementation and testing. |
| R-08 | Medium | Test coverage | The proposed testing is broad but misses explicit tests for cross-layer dependency enforcement, confidence aggregation, rule-publication authorization/audit, API sensitive-log redaction, and Resume Only/shared Resume Quality compatibility. | These gaps leave core ADRs (adjacent layers, confidence separate from score, administrator-only rule publication, safe logging, shared component behavior) unverified. |
| R-09 | Medium | Public interfaces | A complete external output contract is not traceable. Only the Recommendation API is specified; the general Output Engine/API response described by Book 01 and canonical schemas has no endpoint/API contract. | Consumers can receive Recommendation API responses, but the public interface for Score JSON, evidence, confidence, and warnings is undefined. This is an interface gap, not an invitation to invent one. |
| R-10 | Medium | Hidden assumptions | The architecture introduces unapproved operational assumptions: persistent evaluation-report storage, a clock/ID provider, cache behavior, a composition-root DI mechanism, and a concrete observability model. | Most are marked as unspecified technical boundaries, which is appropriate, but they must remain non-binding recommendations until the architect approves them. Persistence is implied by GET-by-evaluation-ID, but its authority, retention, and identity semantics are not defined. |
| R-11 | Medium | Canonical contracts | Canonical object ownership is described, but cross-contract reference integrity and correlation identity are not consistently planned. | Match/Evidence/Score use IDs, while the plan does not provide a contract owner for evaluation IDs, resume IDs, JD IDs, or reference-resolution validation across stages. The handbook names IDs but does not define their generation/lifecycle. |
| R-12 | Low | SOLID | Logical boundaries largely respect single responsibility, but several planned boundaries are overly broad or mixed with adapters. | M08 combines recommendation domain work, report repository, API controller, and response mapping; M01 combines composition, validation, error, and observability. Keep domain ports separate from infrastructure adapters to preserve dependency inversion. This is a structural caution, not a business-rule change. |

## Checks with no finding

- **Handbook chapter coverage:** No Markdown handbook chapter is missing from `TRACEABILITY_MATRIX.md`.
- **Static circular dependency graph:** `ARCHITECTURE.md` does not depict a runtime data-flow cycle. The approved Phase 1 Rule Engine Foundation removes the prior implementation-plan ordering cycle.
- **Core SOLID intent:** The stated parser/entity/feature/matching/evidence/scoring/recommendation separations are aligned with single responsibility and the handbook's explicit engine ownership.
- **Business-logic drift:** The documents do not alter scoring weights, matching thresholds, penalties, or recommendation rules. The unresolved matching order and missing score semantics are correctly surfaced rather than silently selected.

## Required decisions before coding

1. Authoritatively select the matching priority and reconcile it in ADRs, matching handbook, and Rule JSON.
2. Define the valid input boundary for ATS Compatibility and Integrity components so Book 07’s Evidence-JSON-only scoring contract and the component requirements agree.
3. Supply or locate the authoritative rule sets, alias dictionary, ontology, benchmarks, and fixtures.
4. Define the Output Engine and Confidence Aggregator contracts and the public score-output API, or formally limit the public API surface to the supplied recommendation endpoints.
5. Approve or reject the identified infrastructure assumptions before they enter implementation planning.

## Conclusion

The analysis artifacts are a solid handbook-aligned starting point, but the architecture is **not internally complete or ready for coding** until the blockers and high-severity interface/layering issues above are resolved.
