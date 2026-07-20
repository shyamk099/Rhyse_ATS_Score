"""Unit tests for the ProjectScorer.

Purpose:
    Verify deterministic scoring, weights, limits, clamping, and ScoreBreakdown fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary, MatchResult, MatchMetadata
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.project.scorer import ProjectScorer
from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules


def make_mock_proj_result(
    match_id: str,
    resume_feat: str,
    job_feat: str,
    match_type: str = "EXACT_MATCH",
    missing_proj: list[str] | None = None,
) -> MatchResult:
    custom_attrs = {
        "job_project_name": job_feat,
        "resume_project_name": resume_feat,
        "match_type": match_type,
    }
    if missing_proj:
        custom_attrs["missing_projects"] = missing_proj

    return MatchResult(
        match_id=match_id,
        matcher_type="ProjectMatcher",
        resume_feature_id=resume_feat,
        job_feature_id=job_feat,
        metadata=MatchMetadata(
            correlation_id="test-proj",
            matcher_type="ProjectMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes=custom_attrs,
        ),
    )


class ProjectScorerTests(unittest.TestCase):
    """Test suite validating core ProjectScorer point accumulation and DTO builds."""

    def test_score_three_exact_matches(self) -> None:
        results = [
            make_mock_proj_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(3)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: exact_match = 3.0. Expected raw points = 9.0
        rules = ProjectScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ProjectScorer()
        score = scorer.score(context)

        self.assertEqual("PROJECT", score.section_name)
        self.assertEqual(9.0, score.raw_score)
        self.assertEqual(15.0, score.maximum_score)
        self.assertIsNotNone(score.breakdown)
        self.assertEqual(3, score.breakdown.classification_counts.get("exact_match"))
        self.assertEqual(0, score.breakdown.classification_counts.get("similar_project"))

    def test_score_similar_and_related_projects(self) -> None:
        results = [
            make_mock_proj_result("M-1", "R-1", "J-1", match_type="SIMILAR_PROJECT"),
            make_mock_proj_result("M-2", "R-2", "J-2", match_type="RELATED_PROJECT"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: similar = 2.5, related = 2.0. Expected raw points = 4.5
        rules = ProjectScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ProjectScorer()
        score = scorer.score(context)

        self.assertEqual(4.5, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("similar_project"))
        self.assertEqual(1, score.breakdown.classification_counts.get("related_project"))

    def test_score_partial_and_no_matches(self) -> None:
        results = [
            make_mock_proj_result("M-1", "R-1", "J-1", match_type="PARTIAL_MATCH"),
            make_mock_proj_result("M-2", "R-2", "J-2", match_type="NO_MATCH"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Weights: partial = 1.0, no_match = 0.0. Expected raw points = 1.0
        rules = ProjectScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ProjectScorer()
        score = scorer.score(context)

        self.assertEqual(1.0, score.raw_score)
        self.assertEqual(1, score.breakdown.classification_counts.get("partial_match"))

    def test_score_no_projects(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ProjectScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ProjectScorer()
        score = scorer.score(context)

        self.assertEqual(0.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("exact_match"))

    def test_score_clamped_to_maximum(self) -> None:
        results = [
            make_mock_proj_result(f"M-{i}", f"R-{i}", f"J-{i}", match_type="EXACT_MATCH")
            for i in range(10)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Points: 10 * 3.0 = 30.0. Clamped to maximum_project_score = 15.0
        rules = ProjectScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = ProjectScorer()
        score = scorer.score(context)

        self.assertEqual(15.0, score.raw_score)
        self.assertEqual(10, score.breakdown.classification_counts.get("exact_match"))
