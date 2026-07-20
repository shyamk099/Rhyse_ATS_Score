"""Tests for SkillRecommendationProvider.

Purpose:
    Verify SkillRecommendationProvider orchestration, matching result analysis,
    missing skill suggestions, and partial match suggestions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchResult, MatchMetadata, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.recommendation.models import RecommendationContext
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationProviderError

from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
    make_recommendation_context,
)


def make_skill_match_result(
    match_id: str,
    skill_name: str,
    classification: str,
) -> MatchResult:
    """Helper to compile a mock MatchResult with classification details."""
    return MatchResult(
        match_id=match_id,
        matcher_type="SkillMatcher",
        resume_feature_id=skill_name,
        job_feature_id=skill_name,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="SkillMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes={
                "job_skill_name": skill_name,
                "match_classification": classification,
            },
        ),
    )


class SkillRecommendationProviderTests(unittest.TestCase):
    """Test suite validating SkillRecommendationProvider execution."""

    def setUp(self) -> None:
        self.provider = SkillRecommendationProvider()

    def test_provider_identity(self) -> None:
        """Provider must have correct name and priority."""
        self.assertEqual("SKILL", self.provider.provider_name())
        self.assertEqual(100, self.provider.priority())

    def test_validation_missing_skill_score_raises(self) -> None:
        """If ScoreResult doesn't have skill_score, validate() must raise RecommendationProviderError."""
        bad_score_res = ScoreResult(
            overall_score=85.0,
            skill_score=None,  # Missing skill score
            experience_score=SectionScore(section_name="EXPERIENCE", raw_score=10.0, maximum_score=10.0),
            education_score=SectionScore(section_name="EDUCATION", raw_score=10.0, maximum_score=10.0),
            project_score=SectionScore(section_name="PROJECT", raw_score=10.0, maximum_score=10.0),
            certification_score=SectionScore(section_name="CERTIFICATION", raw_score=10.0, maximum_score=10.0),
            statistics=make_mock_score_result().statistics,
            metadata=make_mock_score_result().metadata,
        )
        context = make_recommendation_context(score_result=bad_score_res)
        with self.assertRaises(RecommendationProviderError):
            self.provider.generate(context)

    def test_generate_no_missing_or_partial_skills_returns_empty(self) -> None:
        """If there are no missing or partially matched skills, return empty tuple."""
        context = make_recommendation_context()
        recs = self.provider.generate(context)
        self.assertEqual(0, len(recs))

    def test_generate_one_missing_skill(self) -> None:
        """Must generate exactly one Recommendation DTO for a missing skill."""
        score_res = make_mock_score_result()
        # Add missing skill 'Python' to breakdown
        score_res = score_res.model_copy(
            update={
                "skill_score": SectionScore(
                    section_name="SKILL",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("Python",),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        context = make_recommendation_context(score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("REC-SKILL-MISSING-1", recs[0].recommendation_id)
        self.assertEqual("SKILL_MISSING", recs[0].category)
        self.assertEqual("Python is missing", recs[0].title)

    def test_generate_one_partial_match(self) -> None:
        """Must generate exactly one Recommendation DTO for a partially matched skill."""
        match_result = make_skill_match_result("M-1", "Docker", "SKILL_PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("REC-SKILL-PARTIAL-1", recs[0].recommendation_id)
        self.assertEqual("SKILL_PARTIAL_MATCH", recs[0].category)
        self.assertEqual("Expand Docker experience", recs[0].title)

    def test_generate_multiple_missing_and_partial_skills(self) -> None:
        """Must correctly collate multiple missing and partial skill recommendations."""
        score_res = make_mock_score_result()
        score_res = score_res.model_copy(
            update={
                "skill_score": SectionScore(
                    section_name="SKILL",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("Python", "Git"),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        match_result = make_skill_match_result("M-1", "Docker", "SKILL_PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )

        context = make_recommendation_context(match_collection=match_col, score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(3, len(recs))
        categories = [r.category for r in recs]
        self.assertEqual(["SKILL_MISSING", "SKILL_MISSING", "SKILL_PARTIAL_MATCH"], categories)


if __name__ == "__main__":
    unittest.main()
