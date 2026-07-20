"""Tests for EducationRecommendationProvider.

Purpose:
    Verify EducationRecommendationProvider orchestration, matching result analysis,
    missing education suggestions, and partial match / level gap suggestions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchResult, MatchMetadata, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.recommendation.providers.education_provider import EducationRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationProviderError

from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)


def make_education_match_result(
    match_id: str,
    education_name: str,
    classification: str,
) -> MatchResult:
    """Helper to compile a mock MatchResult with education custom attributes."""
    return MatchResult(
        match_id=match_id,
        matcher_type="EducationMatcher",
        resume_feature_id=education_name,
        job_feature_id=education_name,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="EducationMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes={
                "job_education_name": education_name,
                "match_type": classification,
            },
        ),
    )


class EducationRecommendationProviderTests(unittest.TestCase):
    """Test suite validating EducationRecommendationProvider execution."""

    def setUp(self) -> None:
        self.provider = EducationRecommendationProvider()

    def test_provider_identity(self) -> None:
        """Provider must have correct name and priority."""
        self.assertEqual("EDUCATION", self.provider.provider_name())
        self.assertEqual(300, self.provider.priority())

    def test_validation_missing_education_score_raises(self) -> None:
        """If ScoreResult doesn't have education_score, validate() must raise RecommendationProviderError."""
        bad_score_res = ScoreResult(
            overall_score=85.0,
            skill_score=make_mock_score_result().skill_score,
            experience_score=make_mock_score_result().experience_score,
            education_score=None,  # Missing education score
            project_score=SectionScore(section_name="PROJECT", raw_score=10.0, maximum_score=10.0),
            certification_score=SectionScore(section_name="CERTIFICATION", raw_score=10.0, maximum_score=10.0),
            statistics=make_mock_score_result().statistics,
            metadata=make_mock_score_result().metadata,
        )
        context = make_recommendation_context(score_result=bad_score_res)
        with self.assertRaises(RecommendationProviderError):
            self.provider.generate(context)

    def test_generate_no_gaps_returns_empty(self) -> None:
        """If there are no missing, partial, or level gap educations, return empty tuple."""
        context = make_recommendation_context()
        recs = self.provider.generate(context)
        self.assertEqual(0, len(recs))

    def test_generate_one_missing_education(self) -> None:
        """Must generate exactly one Recommendation DTO for a missing education requirement."""
        score_res = make_mock_score_result()
        # Add missing education 'Bachelor' to breakdown
        score_res = score_res.model_copy(
            update={
                "education_score": SectionScore(
                    section_name="EDUCATION",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("Bachelor",),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        context = make_recommendation_context(score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EDU_MISSING_BACHELOR", recs[0].recommendation_id)
        self.assertEqual("EDUCATION_MISSING", recs[0].category)
        self.assertEqual("Bachelor degree is missing", recs[0].title)

    def test_generate_one_partial_match(self) -> None:
        """Must generate exactly one Recommendation DTO for partially matched education."""
        match_result = make_education_match_result("M-1", "Computer Science", "RELATED_FIELD")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EDU_PARTIAL_COMPUTER_SCIENCE", recs[0].recommendation_id)
        self.assertEqual("EDUCATION_PARTIAL_MATCH", recs[0].category)
        self.assertEqual("Expand Computer Science education details", recs[0].title)

    def test_generate_one_level_gap(self) -> None:
        """Must generate exactly one Recommendation DTO for qualification level gap."""
        match_result = make_education_match_result("M-1", "Masters", "LOWER_THAN_REQUIRED")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("EDU_LEVEL_GAP_MASTERS", recs[0].recommendation_id)
        self.assertEqual("EDUCATION_LEVEL_GAP", recs[0].category)
        self.assertEqual("Upgrade to Masters qualification", recs[0].title)


if __name__ == "__main__":
    unittest.main()
