"""Tests for ProjectRecommendationProvider performance latency.

Purpose:
    Verify that generating project recommendations for 1000 contexts sequentially
    completes within 100ms.
"""

from __future__ import annotations

import time
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


class ProjectProviderLargeDatasetTests(unittest.TestCase):
    """Latency performance tests validating project provider execution budget."""

    ITERATIONS: int = 1000

    def test_large_dataset_project_provider_latency(self) -> None:
        """1000 sequential generate() calls must execute within a 100ms budget."""
        provider = ProjectRecommendationProvider()

        # Build context
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
        context = make_recommendation_context(match_collection=match_col, score_result=score_res)

        start = time.perf_counter()
        for _ in range(self.ITERATIONS):
            provider.generate(context)
        duration_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(
            duration_ms,
            100.0,
            f"Project provider scale latency target exceeded: 1000 runs took {duration_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
