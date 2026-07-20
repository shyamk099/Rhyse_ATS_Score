"""Tests for SkillRecommendationProvider determinism.

Purpose:
    Verify repeated provider execution generates identical recommendation tuples.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from tests.recommendation.providers.test_skill_provider import make_skill_match_result
from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)
from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class SkillProviderDeterminismTests(unittest.TestCase):
    """Tests checking deterministic recommendation generation."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.provider = SkillRecommendationProvider()

        # Build context with 2 missing skills and 1 partial match
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
        self.context = make_recommendation_context(match_collection=match_col, score_result=score_res)

    def test_generation_is_fully_deterministic(self) -> None:
        """Repeated generate() calls must return identical lists of recommendations."""
        first = self.provider.generate(self.context)
        first_titles = [r.title for r in first]

        for _ in range(self.REPETITIONS - 1):
            res = self.provider.generate(self.context)
            res_titles = [r.title for r in res]
            self.assertEqual(first_titles, res_titles)


if __name__ == "__main__":
    unittest.main()
