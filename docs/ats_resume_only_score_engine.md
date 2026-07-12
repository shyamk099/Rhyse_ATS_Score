# ATS Resume Score Engine v3.2 (Resume Only)

> **Algorithm Version:** 3.2
> **Weight Version:** 1.0
> **Semantic Model:** all-MiniLM-L6-v2
> **Calibration Dataset:** Resume Benchmark v1 *(not yet run — see Section 12)*
> **Mode:** Resume Only
> **Input:** Resume
> **Output:** ATS Score (0-100) + Advisory Flag Report
> **Supersedes:** v3.1

---

# 1. Objective

The Resume Only ATS Engine evaluates whether a resume is ATS-friendly without comparing it to any Job Description.

It measures four **scored** pillars — ATS Compatibility, Resume Quality, Language Quality, Semantic Validation — using deterministic rules and embedding-based validation. It separately reports **Advisory Flags**: recruiter-perception and bias-risk signals that inform the candidate but do not move the numeric score.

---

# 2. What Changed in v3.2

| Change | Reason |
|---|---|
| Moved Seniority Fit, Passive Voice, Personal Pronouns → Advisory Layer | These are recruiter-perception checks, not ATS-parsing or content-fact checks. They don't belong in a score meant to represent parseability + verifiable content quality. |
| Renamed *Semantic Evidence Engine* → **Semantic Validation Engine** | Better reflects that this pillar validates claims against evidence, rather than just "finding" evidence. |
| Semantic Validation weight cut 10% → **5%** | No external commercial tool discloses an equivalent check, so there's nothing to calibrate against yet. Weight stays low until validated. |
| The freed 5% + the 7% freed by moving Seniority Fit out of Resume Quality → redistributed into **Resume Quality (40%)** | Content-quality checks (quantified achievements, bullet quality, action verbs) are the most externally-benchmarkable signals available, so they absorb the reallocated weight. |
| Added **Section 12: Calibration Loop** | Makes weight-setting evidence-driven against Resume Worded, Jobscan, Enhancv instead of judgment calls. |
| Added version metadata block | Decouples `Algorithm Version` from `Weight Version` and `Semantic Model`, so weights can be retuned later without invalidating historical scores or requiring a new algorithm version. |

---

# 3. Score Distribution

| Pillar | Weight |
|----------|-------:|
| ATS Compatibility | 40% |
| Resume Quality | 40% |
| Language Quality | 15% |
| Semantic Validation | 5% |

**Total = 100%**

This is intentionally conservative: weight is concentrated in the two pillars (ATS Compatibility, Resume Quality) that can be checked deterministically or benchmarked against commercial tools today. Semantic Validation stays low-weight until Section 12's calibration loop has run at least once.

---

# 4. Architecture

```text
Resume
   │
   ▼
Parser
   │
   ▼
Feature Extraction
   │
   ├── ATS Compatibility (40%)
   ├── Resume Quality (40%)
   ├── Language Quality (15%)
   └── Semantic Validation (5%)
   │
   ▼
Weighted Score Engine
   │
   ▼
ATS Score
   │
   ├── Section Scores
   └── Advisory Flags (Non-scored)
```

---

# 5. ATS Compatibility (40%)

Unchanged. Evaluates whether an ATS can correctly parse the resume.

| Check | Weight |
|----------------------------|------:|
| File Format | 2% |
| File Size | 2% |
| Text Extraction Success | 4% |
| ATS Parseability | 6% |
| Contact Information | 4% |
| Standard Sections | 6% |
| Layout Validation | 5% |
| Header/Footer Detection | 2% |
| Tables / Multi-column Detection | 3% |
| Font Validation | 2% |
| Date Consistency | 2% |
| Resume Length | 2% |

### Checks
PDF/DOCX validation · text extraction · ATS readability · standard section names · email/phone/LinkedIn · single-column layout · no tables/text boxes · standard fonts · consistent dates · professional resume length

---

# 6. Resume Quality (40%)

Seniority Fit has moved to the Advisory Layer (Section 11). The vacated 2%, plus the 5% reassigned from Semantic Validation, is redistributed across the remaining checks — weighted toward the signals most consistently emphasized by commercial tools (quantified achievements, bullet quality, action verbs).

| Check | Weight |
|---------------------------|------:|
| Quantified Achievements | 9% |
| Bullet Quality | 6% |
| Action Verbs | 6% |
| Section Completeness | 6% |
| Career Progression | 4% |
| Leadership Evidence | 3% |
| Project Quality | 3% |
| Resume Completeness | 3% |

**Total: 40%**

### Checks

**Quantified Achievements** — 30%, 2x, $500K, 10 team members

**Bullet Quality** — one idea per bullet, proper length, clear outcome

**Action Verbs** — Built, Designed, Developed, Optimized, Led, Implemented

**Section Completeness** — Summary, Skills, Experience, Education

**Career Progression** — promotion, increasing responsibilities, better role progression

**Leadership Evidence** — mentored, led, managed, coordinated

**Project Quality** — technology used, business outcome, responsibilities, deliverables

**Resume Completeness** — presence of all expected sections for the candidate's level

---

# 7. Language Quality (15%)

Passive Voice and Personal Pronouns have moved to the Advisory Layer. The vacated 2% is redistributed back into Grammar and Readability — this restores the original v3.0 weighting, since those two checks are the most deterministic (rule-based) signals in this pillar.

| Check | Weight |
|--------------------|------:|
| Grammar | 5% |
| Spelling | 3% |
| Readability | 3% |
| Weak Words | 2% |
| Repeated Words | 1% |
| Buzzwords | 1% |

**Total: 15%**

### Checks
Grammar · Spelling · sentence clarity · weak phrases ("responsible for," "worked on," "helped") · repeated words · buzzwords ("hardworking," "team player," "go-getter")

---

# 8. Semantic Validation Engine (5%)

Renamed from *Semantic Evidence Engine*. Validates whether claimed skills are supported by resume evidence using embeddings rather than exact keyword overlap. Weight halved from v3.1 pending calibration — see Section 12.

## Workflow

```text
Extract Skills
      │
      ▼
Generate Skill Embeddings
      │
      ▼
Generate Experience Embeddings
      │
      ▼
Vector Similarity Search
      │
      ▼
Evidence Validation
      │
      ▼
Semantic Score
```

## Semantic Checks

| Check | Weight |
|-------------------------------|------:|
| Skill ↔ Experience Evidence | 2.0% |
| Skill ↔ Project Evidence | 1.0% |
| Skill ↔ Certification Evidence | 0.5% |
| Summary ↔ Resume Consistency | 1.0% |
| Contradictory / Duplicate Claims | 0.5% |

**Total: 5%**

### Example

| Skill | Evidence |
|---------|----------|
| AWS | ✅ |
| PySpark | ✅ |
| SQL | ❌ |
| Databricks | ❌ |

> **Why the weight is low:** no reference tool reviewed (Resume Worded, Enhancv, MyPerfectResume, GoodSpace, Jobscan, HireFlow) discloses an embedding-based skill-to-evidence check — their "semantic" language reads as rule/phrase-based. This pillar has no external benchmark, so it stays low-weight and gets validated against manually labeled resume/skill pairs rather than competitor-score comparison, until Section 12's loop provides evidence to raise it.

---

# 9. Final Formula

```
ATS Score

=

40% ATS Compatibility

+

40% Resume Quality

+

15% Language Quality

+

5% Semantic Validation
```

---

# 10. Output

```json
{
    "algorithm_version": "3.2",
    "weight_version": "1.0",
    "overall_score": 84,
    "ats_compatibility": 87,
    "resume_quality": 83,
    "language_quality": 90,
    "semantic_validation": 78,
    "advisory_flags": [
        {
            "type": "SENIORITY_MISMATCH",
            "detail": "Title 'Senior Data Engineer' but no bullet shows scope beyond individual contributor work."
        },
        {
            "type": "PASSIVE_VOICE",
            "detail": "3 bullets use passive constructions (e.g. 'was responsible for managing')."
        },
        {
            "type": "PERSONAL_PRONOUN",
            "detail": "First-person pronoun found in Summary section."
        }
    ]
}
```

`advisory_flags` is additive metadata. It never changes `overall_score`.

---

# 11. Advisory Layer (Non-Scored)

Recruiter-perception and bias-risk signals live here, not in the score, because they represent judgment calls about how a human might read the resume rather than deterministic facts about parseability or content quality. Scoring them would mean silently asserting recruiter bias as ground truth (e.g. penalizing an older graduation date).

| Flag Type | Example Trigger |
|---|---|
| `SENIORITY_MISMATCH` | Title/scope language inconsistent with years of experience |
| `PASSIVE_VOICE` | Constructions like "was responsible for managing" instead of "managed" |
| `PERSONAL_PRONOUN` | First-person pronouns ("I," "my") in a document that conventionally omits them |
| `AGE_BIAS_RISK` | Graduation date implies age; large gap between education and first job |
| `AMBIGUOUS_CLAIM` | Achievement stated without metric, scope, or outcome ("improved processes") |
| `EMPLOYMENT_GAP` | Unexplained gap of 6+ months between roles |
| `TITLE_INFLATION_RISK` | Self-assigned or non-standard title with no external verification signal |

---

# 12. Calibration Loop

Weights in this document (Weight Version 1.0) are a starting point, not a finished result. They get adjusted through a repeatable, evidence-driven loop rather than further judgment calls:

```text
Benchmark Resumes
        │
        ▼
  Run Resume Worded
  Run Jobscan
  Run Enhancv
  Run Our Engine
        │
        ▼
  Compare Scores
        │
        ▼
  Adjust Weights
        │
        ▼
  Freeze Version
```

**How this works:**
1. Assemble a fixed benchmark set of resumes (`Resume Benchmark v1`) spanning a spread of quality — deliberately bad, average, and strong resumes.
2. Run each resume through Resume Worded, Jobscan, and Enhancv, and record their scores.
3. Run the same resumes through this engine.
4. Compare **rank order and direction**, not absolute score parity — Section 12 of v3.1's research confirmed no vendor discloses its actual weight formula, so exact numeric matching isn't a valid target. The bar is: does a resume that scores low on Jobscan also score low here, and does a resume that scores high stay high?
5. Where directional agreement breaks down, adjust sub-check weights within a pillar (not pillar-level weights, unless the disagreement is systemic).
6. Once a weight set produces consistent directional agreement across the benchmark set, increment `Weight Version` and freeze it. Past scores generated under a prior `Weight Version` remain valid under that version's number — they are not silently invalidated by future recalibration.

This loop is what should eventually justify raising Semantic Validation's weight above 5%: once it's been run against labeled resume/skill pairs (see Section 8) with measurable precision, not before.

---

# 13. Scope

This engine performs only ATS scoring and advisory flagging.

It does **not** include

- Job Description Matching
- Keyword Matching
- Resume Optimization
- Resume Rewriting
- Recommendation Generation
- AI Resume Enhancement

Those belong to the Resume + JD engine (future work).