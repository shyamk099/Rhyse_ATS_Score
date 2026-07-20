"""Unit tests for the ExperienceScorer.

Purpose:
    Verify deterministic scoring, weights, limits, clamping, and ScoreBreakdown fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary, MatchResult, MatchMetadata
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules


def make_mock_exp_result(
    match_id: str,
    resume_feat: str,
    job_feat: str,
    match_type: str = "EXACT_MATCH",
    missing_exp: list[str] | None = None,
) -> MatchResult:
    custom_attrs = {
        "job_experience_name": job_feat,
        "resume_experience_name": resume_feat,
        "match_type": match_type,
    }
    if missing_exp:
        custom_attrs["missing_experience"] = missing_exp

    return MatchResult(
        match_id=match_id,
        matcher_type="ExperienceMatcher",
        resume_feature_id=resume_feat,
        job_feature_id=job_feat,
        metadata=MatchMetadata(
            correlation_id="test-exp",
            matcher_type="ExperienceMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes=custom_attrs,
        ),
    )


class ExperienceScorerTests(unittest.TestCase):
    """Test suite validating core ExperienceScorer point accumulation and DTO builds."""

    def test_score_five_exact_matches(self) -> None:
        results = [
            make_mock_exp_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(5)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: exact_match = 3.0. Clamped to maximum_experience_score = 25.0
        rules = ExperienceScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ExperienceScorer()
        score = scorer.score(context)

        self.assertEqual("EXPERIENCE", score.section_name)
        self.assertEqual(15.0, score.raw_score)
        self.assertEqual(25.0, score.maximum_score)
        self.assertIsNotNone(score.breakdown)
        self.assertEqual(5, score.breakdown.classification_counts.get("exact_match"))
        self.assertEqual(0, score.breakdown.classification_counts.get("partial_match"))

    def test_score_only_partial_matches(self) -> None:
        results = [
            make_mock_exp_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="PARTIAL_MATCH")
            for i in range(4)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: partial = 1.5. Expected raw points = 6.0
        rules = ExperienceScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ExperienceScorer()
        score = scorer.score(context)

        self.assertEqual(6.0, score.raw_score)
        self.assertEqual(4, score.breakdown.classification_counts.get("partial_match"))

    def test_score_overqualified_and_underqualified(self) -> None:
        results = [
            make_mock_exp_result("M-1", "R-1", "J-1", match_type="OVERQUALIFIED"),
            make_mock_exp_result("M-2", "R-2", "J-2", match_type="UNDERQUALIFIED"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: overqualified = 3.0, underqualified = 0.5. Expected raw points = 3.5
        rules = ExperienceScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ExperienceScorer()
        score = scorer.score(context)

        self.assertEqual(3.5, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("overqualified"))
        self.assertEqual(1, score.breakdown.classification_counts.get("underqualified"))

    def test_score_no_experience_matches(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ExperienceScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ExperienceScorer()
        score = scorer.score(context)

        self.assertEqual(0.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("exact_match"))

    def test_score_clamped_to_maximum(self) -> None:
        results = [
            make_mock_exp_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(15)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Points: 15 * 3.0 = 45.0. Clamped to maximum_experience_score = 25.0
        rules = ExperienceScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ExperienceScorer()
        score = scorer.score(context)

        self.assertEqual(25.0, score.raw_score)
        self.assertEqual(15, score.breakdown.classification_counts.get("exact_match"))
