"""Unit tests for the EducationScorer.

Purpose:
    Verify deterministic scoring, weights, limits, clamping, and ScoreBreakdown fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary, MatchResult, MatchMetadata
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.education.scorer import EducationScorer
from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules


def make_mock_edu_result(
    match_id: str,
    resume_feat: str,
    job_feat: str,
    match_type: str = "EXACT_MATCH",
    missing_edu: list[str] | None = None,
) -> MatchResult:
    custom_attrs = {
        "job_education_name": job_feat,
        "resume_experience_name": resume_feat,
        "match_type": match_type,
    }
    if missing_edu:
        custom_attrs["missing_education"] = missing_edu

    return MatchResult(
        match_id=match_id,
        matcher_type="EducationMatcher",
        resume_feature_id=resume_feat,
        job_feature_id=job_feat,
        metadata=MatchMetadata(
            correlation_id="test-edu",
            matcher_type="EducationMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes=custom_attrs,
        ),
    )


class EducationScorerTests(unittest.TestCase):
    """Test suite validating core EducationScorer point accumulation and DTO builds."""

    def test_score_three_exact_matches(self) -> None:
        results = [
            make_mock_edu_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(3)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: exact_match = 4.0. Expected raw points = 12.0
        rules = EducationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = EducationScorer()
        score = scorer.score(context)

        self.assertEqual("EDUCATION", score.section_name)
        self.assertEqual(12.0, score.raw_score)
        self.assertEqual(15.0, score.maximum_score)
        self.assertIsNotNone(score.breakdown)
        self.assertEqual(3, score.breakdown.classification_counts.get("exact_match"))
        self.assertEqual(0, score.breakdown.classification_counts.get("higher_than_required"))

    def test_score_higher_and_related_fields(self) -> None:
        results = [
            make_mock_edu_result("M-1", "R-1", "J-1", match_type="HIGHER_THAN_REQUIRED"),
            make_mock_edu_result("M-2", "R-2", "J-2", match_type="RELATED_FIELD"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: higher = 4.0, related = 2.5. Expected raw points = 6.5
        rules = EducationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = EducationScorer()
        score = scorer.score(context)

        self.assertEqual(6.5, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("higher_than_required"))
        self.assertEqual(1, score.breakdown.classification_counts.get("related_field"))

    def test_score_lower_and_unrelated_fields(self) -> None:
        results = [
            make_mock_edu_result("M-1", "R-1", "J-1", match_type="LOWER_THAN_REQUIRED"),
            make_mock_edu_result("M-2", "R-2", "J-2", match_type="UNRELATED_FIELD"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: lower = 1.0, unrelated = 0.0. Expected raw points = 1.0
        rules = EducationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = EducationScorer()
        score = scorer.score(context)

        self.assertEqual(1.0, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("lower_than_required"))
        self.assertEqual(1, score.breakdown.classification_counts.get("unrelated_field"))

    def test_score_no_education(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = EducationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = EducationScorer()
        score = scorer.score(context)

        self.assertEqual(0.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("exact_match"))

    def test_score_clamped_to_maximum(self) -> None:
        results = [
            make_mock_edu_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(10)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Points: 10 * 4.0 = 40.0. Clamped to maximum_education_score = 15.0
        rules = EducationScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = EducationScorer()
        score = scorer.score(context)

        self.assertEqual(15.0, score.raw_score)
        self.assertEqual(10, score.breakdown.classification_counts.get("exact_match"))
