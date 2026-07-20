"""Unit tests for the CertificationScorer.

Purpose:
    Verify deterministic scoring, weights, limits, clamping, and ScoreBreakdown fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary, MatchResult, MatchMetadata
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.certification.scorer import CertificationScorer
from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules


def make_mock_cert_result(
    match_id: str,
    resume_feat: str,
    job_feat: str,
    match_type: str = "EXACT_MATCH",
    missing_cert: list[str] | None = None,
) -> MatchResult:
    custom_attrs = {
        "job_certification_name": job_feat,
        "resume_certification_name": resume_feat,
        "match_type": match_type,
    }
    if missing_cert:
        custom_attrs["missing_certifications"] = missing_cert

    return MatchResult(
        match_id=match_id,
        matcher_type="CertificationMatcher",
        resume_feature_id=resume_feat,
        job_feature_id=job_feat,
        metadata=MatchMetadata(
            correlation_id="test-cert",
            matcher_type="CertificationMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes=custom_attrs,
        ),
    )


class CertificationScorerTests(unittest.TestCase):
    """Test suite validating core CertificationScorer point accumulation and DTO builds."""

    def test_score_three_exact_matches(self) -> None:
        results = [
            make_mock_cert_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(3)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: exact_match = 3.0. Expected raw points = 9.0
        rules = CertificationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = CertificationScorer()
        score = scorer.score(context)

        self.assertEqual("CERTIFICATION", score.section_name)
        self.assertEqual(9.0, score.raw_score)
        self.assertEqual(10.0, score.maximum_score)
        self.assertIsNotNone(score.breakdown)
        self.assertEqual(3, score.breakdown.classification_counts.get("exact_match"))
        self.assertEqual(0, score.breakdown.classification_counts.get("equivalent_certification"))

    def test_score_equivalent_and_related_certifications(self) -> None:
        results = [
            make_mock_cert_result("M-1", "R-1", "J-1", match_type="EQUIVALENT_CERTIFICATION"),
            make_mock_cert_result("M-2", "R-2", "J-2", match_type="RELATED_CERTIFICATION"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: equivalent = 2.5, related = 2.0. Expected raw points = 4.5
        rules = CertificationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = CertificationScorer()
        score = scorer.score(context)

        self.assertEqual(4.5, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("equivalent_certification"))
        self.assertEqual(1, score.breakdown.classification_counts.get("related_certification"))

    def test_score_partial_and_expired_certifications(self) -> None:
        results = [
            make_mock_cert_result("M-1", "R-1", "J-1", match_type="PARTIAL_MATCH"),
            make_mock_cert_result("M-2", "R-2", "J-2", match_type="EXPIRED_CERTIFICATION"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: partial = 1.0, expired = 0.5. Expected raw points = 1.5
        rules = CertificationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = CertificationScorer()
        score = scorer.score(context)

        self.assertEqual(1.5, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("partial_match"))
        self.assertEqual(1, score.breakdown.classification_counts.get("expired_certification"))

    def test_score_no_certifications(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = CertificationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = CertificationScorer()
        score = scorer.score(context)

        self.assertEqual(0.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("exact_match"))

    def test_score_clamped_to_maximum(self) -> None:
        results = [
            make_mock_cert_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(10)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Points: 10 * 3.0 = 30.0. Clamped to maximum_certification_score = 10.0
        rules = CertificationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = CertificationScorer()
        score = scorer.score(context)

        self.assertEqual(10.0, score.raw_score)
        self.assertEqual(10, score.breakdown.classification_counts.get("exact_match"))
