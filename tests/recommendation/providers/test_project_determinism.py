"""Tests for ProjectRecommendationProvider determinism.

Purpose:
    Verify repeated provider execution generates identical recommendation DTO lists.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.project_provider import ProjectRecommendationProvider
from tests.recommendation.providers.test_project_provider import make_project_match_result
from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)
from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class ProjectProviderDeterminismTests(unittest.TestCase):
    """Tests checking deterministic recommendation generation for project provider."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.provider = ProjectRecommendationProvider()

        # Build context with 1 missing project and 1 partial match
        score_res = make_mock_score_result()
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
        match_result = make_project_match_result("M-1", "Event Driven", "PARTIAL_MATCH")
        match_col = CanonicalMatchCollection(
            results=(match_result,),
            statistics=make_mock_match_collection().statistics,
            validation_summary=make_mock_match_collection().validation_summary,
        )
        self.context = make_recommendation_context(match_collection=match_col, score_result=score_res)

    def test_generation_is_fully_deterministic(self) -> None:
        """Repeated generate() calls must return identical lists of recommendations."""
        first = self.provider.generate(self.context)
        first_ids = [r.recommendation_id for r in first]

        for _ in range(self.REPETITIONS - 1):
            res = self.provider.generate(self.context)
            res_ids = [r.recommendation_id for r in res]
            self.assertEqual(first_ids, res_ids)


if __name__ == "__main__":
    unittest.main()
