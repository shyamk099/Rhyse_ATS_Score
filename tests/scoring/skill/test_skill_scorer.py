"""Unit tests for the SkillScorer.

Purpose:
    Verify deterministic scoring, weights, limits, clamping, and ScoreBreakdown fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary, MatchResult, MatchMetadata
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules


def make_mock_result(
    match_id: str,
    resume_feat: str,
    job_feat: str,
    is_mandatory: bool = False,
    missing_skills: list[str] | None = None,
) -> MatchResult:
    custom_attrs = {
        "job_skill_name": job_feat,
        "resume_skill_name": resume_feat,
    }
    if is_mandatory:
        custom_attrs["is_mandatory"] = True
    if missing_skills:
        custom_attrs["missing_skills"] = missing_skills

    return MatchResult(
        match_id=match_id,
        matcher_type="SkillMatcher",
        resume_feature_id=resume_feat,
        job_feature_id=job_feat,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="SkillMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes=custom_attrs,
        ),
    )


class SkillScorerTests(unittest.TestCase):
    """Test suite validating core SkillScorer point accumulation and DTO builds."""

    def test_score_five_mandatory_skills(self) -> None:
        results = [
            make_mock_result(f"M-{i}", f"R-{i}", f"J-{i}", is_mandatory=True)
            for i in range(5)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: mandatory = 2.0. Expected raw points = 10.0
        rules = SkillScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = SkillScorer()
        score = scorer.score(context)

        self.assertEqual("SKILL", score.section_name)
        self.assertEqual(10.0, score.raw_score)
        self.assertEqual(40.0, score.maximum_score)
        self.assertIsNotNone(score.breakdown)
        self.assertEqual(5, score.breakdown.classification_counts.get("mandatory"))
        self.assertEqual(0, score.breakdown.classification_counts.get("optional"))

    def test_score_only_optional_skills(self) -> None:
        results = [
            make_mock_result(f"M-{i}", f"R-{i}", f"J-{i}", is_mandatory=False)
            for i in range(5)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Default weights: optional = 1.0. Expected raw points = 5.0
        rules = SkillScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = SkillScorer()
        score = scorer.score(context)

        self.assertEqual(5.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("mandatory"))
        self.assertEqual(5, score.breakdown.classification_counts.get("optional"))

    def test_score_mixed_skills(self) -> None:
        results = [
            make_mock_result("M-1", "R-1", "J-1", is_mandatory=True),
            make_mock_result("M-2", "R-2", "J-2", is_mandatory=True),
            make_mock_result("M-3", "R-3", "J-3", is_mandatory=True),
            make_mock_result("M-4", "R-4", "J-4", is_mandatory=False),
            make_mock_result("M-5", "R-5", "J-5", is_mandatory=False),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Expected points: 3 * 2.0 + 2 * 1.0 = 8.0
        rules = SkillScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = SkillScorer()
        score = scorer.score(context)

        self.assertEqual(8.0, score.raw_score)
        self.assertEqual(3, score.breakdown.classification_counts.get("mandatory"))
        self.assertEqual(2, score.breakdown.classification_counts.get("optional"))

    def test_score_no_skills(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = SkillScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = SkillScorer()
        score = scorer.score(context)

        self.assertEqual(0.0, score.raw_score)
        self.assertEqual(0, score.breakdown.classification_counts.get("mandatory"))
        self.assertEqual(0, score.breakdown.classification_counts.get("optional"))

    def test_score_clamped_to_maximum(self) -> None:
        results = [
            make_mock_result(f"M-{i}", f"R-{i}", f"J-{i}", is_mandatory=True)
            for i in range(30)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        # Points: 30 * 2.0 = 60.0. Clamped to maximum_skill_score = 40.0
        rules = SkillScoringRules()
        context = ScoringContext(match_collection=col, rules=rules)

        scorer = SkillScorer()
        score = scorer.score(context)

        self.assertEqual(40.0, score.raw_score)
        self.assertEqual(30, score.breakdown.classification_counts.get("mandatory"))
