"""Tests for CertificationRecommendationProvider performance latency.

Purpose:
    Verify that generating certification recommendations for 1000 contexts sequentially
    completes within 100ms.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.recommendation.providers.certification_provider import CertificationRecommendationProvider
from tests.recommendation.providers.test_certification_provider import make_certification_match_result
from tests.recommendation.helpers import (
    make_mock_match_collection,
    make_mock_score_result,
    make_recommendation_context,
)
from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class CertificationProviderLargeDatasetTests(unittest.TestCase):
    """Latency performance tests validating certification provider execution budget."""

    ITERATIONS: int = 1000

    def test_large_dataset_certification_provider_latency(self) -> None:
        """1000 sequential generate() calls must execute within a 100ms budget."""
        provider = CertificationRecommendationProvider()

        # Build context
        score_res = make_mock_score_result()
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
        match_result = make_certification_match_result("M-1", "Azure Administrator", "PARTIAL_MATCH")
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
            f"Certification provider scale latency target exceeded: 1000 runs took {duration_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
