"""Tests for CertificationRecommendationProvider.

Purpose:
    Verify CertificationRecommendationProvider orchestration, matching result analysis,
    missing certification suggestions, and partial match / expired suggestions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchResult, MatchMetadata, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.recommendation.providers.certification_provider import CertificationRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationProviderError

from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)


def make_certification_match_result(
    match_id: str,
    certification_name: str,
    classification: str,
) -> MatchResult:
    """Helper to compile a mock MatchResult with certification custom attributes."""
    return MatchResult(
        match_id=match_id,
        matcher_type="CertificationMatcher",
        resume_feature_id=certification_name,
        job_feature_id=certification_name,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="CertificationMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes={
                "job_certification_name": certification_name,
                "match_type": classification,
            },
        ),
    )


class CertificationRecommendationProviderTests(unittest.TestCase):
    """Test suite validating CertificationRecommendationProvider execution."""

    def setUp(self) -> None:
        self.provider = CertificationRecommendationProvider()

    def test_provider_identity(self) -> None:
        """Provider must have correct name and priority."""
        self.assertEqual("CERTIFICATION", self.provider.provider_name())
        self.assertEqual(500, self.provider.priority())

    def test_validation_missing_certification_score_raises(self) -> None:
        """If ScoreResult doesn't have certification_score, validate() must raise RecommendationProviderError."""
        bad_score_res = ScoreResult(
            overall_score=85.0,
            skill_score=make_mock_score_result().skill_score,
            experience_score=make_mock_score_result().experience_score,
            education_score=make_mock_score_result().education_score,
            project_score=make_mock_score_result().project_score,
            certification_score=None,  # Missing certification score
            statistics=make_mock_score_result().statistics,
            metadata=make_mock_score_result().metadata,
        )
        context = make_recommendation_context(score_result=bad_score_res)
        with self.assertRaises(RecommendationProviderError):
            self.provider.generate(context)

    def test_generate_no_gaps_returns_empty(self) -> None:
        """If there are no missing, partial, or expired certifications, return empty tuple."""
        context = make_recommendation_context()
        recs = self.provider.generate(context)
        self.assertEqual(0, len(recs))

    def test_generate_one_missing_certification(self) -> None:
        """Must generate exactly one Recommendation DTO for a missing certification requirement."""
        score_res = make_mock_score_result()
        # Add missing certification 'AWS SAA' to breakdown
        score_res = score_res.model_copy(
            update={
                "certification_score": SectionScore(
                    section_name="CERTIFICATION",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("AWS SAA",),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        context = make_recommendation_context(score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("CERT_MISSING_AWS_SAA", recs[0].recommendation_id)
        self.assertEqual("CERTIFICATION_MISSING", recs[0].category)
        self.assertEqual("AWS SAA certification is missing", recs[0].title)

    def test_generate_one_partial_match(self) -> None:
        """Must generate exactly one Recommendation DTO for partially matched certification."""
        match_result = make_certification_match_result("M-1", "Azure Administrator", "PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("CERT_PARTIAL_AZURE_ADMINISTRATOR", recs[0].recommendation_id)
        self.assertEqual("CERTIFICATION_PARTIAL_MATCH", recs[0].category)
        self.assertEqual("Expand Azure Administrator details", recs[0].title)

    def test_generate_one_expired(self) -> None:
        """Must generate exactly one Recommendation DTO for expired certification."""
        match_result = make_certification_match_result("M-1", "PMP", "EXPIRED_CERTIFICATION")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("CERT_EXPIRED_PMP", recs[0].recommendation_id)
        self.assertEqual("CERTIFICATION_EXPIRED", recs[0].category)
        self.assertEqual("Renew PMP certification", recs[0].title)


if __name__ == "__main__":
    unittest.main()
