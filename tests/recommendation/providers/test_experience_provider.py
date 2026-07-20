"""Tests for ExperienceRecommendationProvider.

Purpose:
    Verify ExperienceRecommendationProvider orchestration, matching result analysis,
    missing experience suggestions, and partial match / duration gap suggestions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchResult, MatchMetadata, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationProviderError

from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)


def make_experience_match_result(
    match_id: str,
    experience_name: str,
    classification: str,
    duration_gap: bool = False,
) -> MatchResult:
    """Helper to compile a mock MatchResult with experience custom attributes."""
    return MatchResult(
        match_id=match_id,
        matcher_type="ExperienceMatcher",
        resume_feature_id=experience_name,
        job_feature_id=experience_name,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="ExperienceMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes={
                "job_experience_name": experience_name,
                "match_type": classification,
                "duration_gap": duration_gap,
            },
        ),
    )


class ExperienceRecommendationProviderTests(unittest.TestCase):
    """Test suite validating ExperienceRecommendationProvider execution."""

    def setUp(self) -> None:
        self.provider = ExperienceRecommendationProvider()

    def test_provider_identity(self) -> None:
        """Provider must have correct name and priority."""
        self.assertEqual("EXPERIENCE", self.provider.provider_name())
        self.assertEqual(200, self.provider.priority())

    def test_validation_missing_experience_score_raises(self) -> None:
        """If ScoreResult doesn't have experience_score, validate() must raise RecommendationProviderError."""
        bad_score_res = ScoreResult(
            overall_score=85.0,
            skill_score=make_mock_score_result().skill_score,
            experience_score=None,  # Missing experience score
            education_score=SectionScore(section_name="EDUCATION", raw_score=10.0, maximum_score=10.0),
            project_score=SectionScore(section_name="PROJECT", raw_score=10.0, maximum_score=10.0),
            certification_score=SectionScore(section_name="CERTIFICATION", raw_score=10.0, maximum_score=10.0),
            statistics=make_mock_score_result().statistics,
            metadata=make_mock_score_result().metadata,
        )
        context = make_recommendation_context(score_result=bad_score_res)
        with self.assertRaises(RecommendationProviderError):
            self.provider.generate(context)

    def test_generate_no_gaps_returns_empty(self) -> None:
        """If there are no missing, partial, or duration gap experiences, return empty tuple."""
        context = make_recommendation_context()
        recs = self.provider.generate(context)
        self.assertEqual(0, len(recs))

    def test_generate_one_missing_experience(self) -> None:
        """Must generate exactly one Recommendation DTO for a missing experience requirement."""
        score_res = make_mock_score_result()
        # Add missing experience 'Cloud Architecture' to breakdown
        score_res = score_res.model_copy(
            update={
                "experience_score": SectionScore(
                    section_name="EXPERIENCE",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("Cloud Architecture",),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        context = make_recommendation_context(score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EXP_MISSING_CLOUD_ARCHITECTURE", recs[0].recommendation_id)
        self.assertEqual("EXPERIENCE_MISSING", recs[0].category)
        self.assertEqual("Cloud Architecture experience is missing", recs[0].title)

    def test_generate_one_partial_match(self) -> None:
        """Must generate exactly one Recommendation DTO for partially matched experience."""
        match_result = make_experience_match_result("M-1", "Kubernetes", "PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EXP_PARTIAL_KUBERNETES", recs[0].recommendation_id)
        self.assertEqual("EXPERIENCE_PARTIAL_MATCH", recs[0].category)
        self.assertEqual("Expand Kubernetes experience", recs[0].title)

    def test_generate_one_duration_gap(self) -> None:
        """Must generate exactly one Recommendation DTO for duration gap."""
        match_result = make_experience_match_result("M-1", "Docker", "UNDERQUALIFIED")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EXP_DURATION_DOCKER", recs[0].recommendation_id)
        self.assertEqual("EXPERIENCE_DURATION_GAP", recs[0].category)
        self.assertEqual("Increase Docker duration", recs[0].title)


if __name__ == "__main__":
    unittest.main()
