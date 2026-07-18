# Experience Matching Sequence Diagram

## Book 05 — Matching Engine | Milestone 5.3

The sequence diagram details pipeline calls executing the ExperienceMatcher:

```mermaid
sequenceDiagram
    autonumber
    participant Pipeline as MatchingPipeline
    participant Matcher as ExperienceMatcher
    participant Candidate as ExperienceMatchCandidateBuilder
    participant Validator as ExperienceMatchValidator
    participant Normalizer as ExperienceMatchNormalizer
    participant Builder as ExperienceMatchBuilder

    Pipeline ->> Matcher: match(resume, job, context)
    Matcher ->> Candidate: build_candidates(resume, job, rules)
    Candidate -->> Matcher: Sequence[ExperienceMatchCandidate]
    Loop over candidates
        Matcher ->> Validator: validate(candidate, rules)
        Validator -->> Matcher: errors
        Matcher ->> Normalizer: normalize(candidate, rules)
        Normalizer -->> Matcher: normalized_candidate
        Note over Matcher: Check canonical ID matching first (precedence)<br/>Fallback to company & title matching if IDs are missing
        Matcher ->> Builder: build(normalized_candidate, context)
        Builder -->> Matcher: MatchResult
    End
    Note over Matcher: Sort MatchResults deterministically by matcher_type, resume_feature_id, and job_feature_id
    Matcher -->> Pipeline: Sequence[MatchResult]
```
