"""Tests for CertificationRecommendationProvider thread safety.

Purpose:
    Verify concurrent generate() executions return isolated recommendation DTO lists.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

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


class CertificationProviderThreadSafetyTests(unittest.TestCase):
    """Tests checking concurrent execution safety for certification provider."""

    THREAD_COUNT: int = 20

    def setUp(self) -> None:
        self.provider = CertificationRecommendationProvider()

        # Build context with 1 missing certification and 1 partial match
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
        self.context = make_recommendation_context(match_collection=match_col, score_result=score_res)

    def test_concurrent_generate_calls_are_isolated(self) -> None:
        """All threads executing generate() concurrently must succeed with independent DTO lists."""
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = self.provider.generate(self.context)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for r in results:
            self.assertEqual(2, len(r))

        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))


if __name__ == "__main__":
    unittest.main()
