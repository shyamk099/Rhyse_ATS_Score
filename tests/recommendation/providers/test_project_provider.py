"""Tests for ProjectRecommendationProvider.

Purpose:
    Verify ProjectRecommendationProvider orchestration, matching result analysis,
    missing project suggestions, and partial match / related gap suggestions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchResult, MatchMetadata, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.recommendation.providers.project_provider import ProjectRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationProviderError

from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)


def make_project_match_result(
    match_id: str,
    project_name: str,
    classification: str,
) -> MatchResult:
    """Helper to compile a mock MatchResult with project custom attributes."""
    return MatchResult(
        match_id=match_id,
        matcher_type="ProjectMatcher",
        resume_feature_id=project_name,
        job_feature_id=project_name,
        metadata=MatchMetadata(
            correlation_id="test",
            matcher_type="ProjectMatcher",
            execution_timestamp="2026-07-19T00:00:00Z",
            rules_version="1.0.0",
            custom_attributes={
                "job_project_name": project_name,
                "match_type": classification,
            },
        ),
    )


class ProjectRecommendationProviderTests(unittest.TestCase):
    """Test suite validating ProjectRecommendationProvider execution."""

    def setUp(self) -> None:
        self.provider = ProjectRecommendationProvider()

    def test_provider_identity(self) -> None:
        """Provider must have correct name and priority."""
        self.assertEqual("PROJECT", self.provider.provider_name())
        self.assertEqual(400, self.provider.priority())

    def test_validation_missing_project_score_raises(self) -> None:
        """If ScoreResult doesn't have project_score, validate() must raise RecommendationProviderError."""
        bad_score_res = ScoreResult(
            overall_score=85.0,
            skill_score=make_mock_score_result().skill_score,
            experience_score=make_mock_score_result().experience_score,
            education_score=make_mock_score_result().education_score,
            project_score=None,  # Missing project score
            certification_score=SectionScore(section_name="CERTIFICATION", raw_score=10.0, maximum_score=10.0),
            statistics=make_mock_score_result().statistics,
            metadata=make_mock_score_result().metadata,
        )
        context = make_recommendation_context(score_result=bad_score_res)
        with self.assertRaises(RecommendationProviderError):
            self.provider.generate(context)

    def test_generate_no_gaps_returns_empty(self) -> None:
        """If there are no missing, partial, or related gap projects, return empty tuple."""
        context = make_recommendation_context()
        recs = self.provider.generate(context)
        self.assertEqual(0, len(recs))

    def test_generate_one_missing_project(self) -> None:
        """Must generate exactly one Recommendation DTO for a missing project requirement."""
        score_res = make_mock_score_result()
        # Add missing project 'Microservices' to breakdown
        score_res = score_res.model_copy(
            update={
                "project_score": SectionScore(
                    section_name="PROJECT",
                    raw_score=10.0,
                    maximum_score=20.0,
                    breakdown=ScoreBreakdown(
                        missing_items=("Microservices",),
                        rules_version="1.0.0",
                    ),
                )
            }
        )
        context = make_recommendation_context(score_result=score_res)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("PROJ_MISSING_MICROSERVICES", recs[0].recommendation_id)
        self.assertEqual("PROJECT_MISSING", recs[0].category)
        self.assertEqual("Microservices project is missing", recs[0].title)

    def test_generate_one_partial_match(self) -> None:
        """Must generate exactly one Recommendation DTO for partially matched project."""
        match_result = make_project_match_result("M-1", "Event Driven", "PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("PROJ_PARTIAL_EVENT_DRIVEN", recs[0].recommendation_id)
        self.assertEqual("PROJECT_PARTIAL_MATCH", recs[0].category)
        self.assertEqual("Expand Event Driven project details", recs[0].title)

    def test_generate_one_related_gap(self) -> None:
        """Must generate exactly one Recommendation DTO for related project gap."""
        match_result = make_project_match_result("M-1", "Cloud Native", "RELATED_PROJECT")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        context = make_recommendation_context(match_collection=match_col)
        recs = self.provider.generate(context)

        self.assertEqual(1, len(recs))
        self.assertEqual("PROJ_RELATED_CLOUD_NATIVE", recs[0].recommendation_id)
        self.assertEqual("PROJECT_RELATED_GAP", recs[0].category)
        self.assertEqual("Add related Cloud Native project", recs[0].title)


if __name__ == "__main__":
    unittest.main()
