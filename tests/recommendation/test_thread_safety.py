"""Tests for thread-safe concurrent recommendation execution.

Purpose:
    Verify that multiple threads can invoke RecommendationEngine.recommend()
    concurrently on the same engine/inputs and each receives an isolated result.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.models import RecommendationResult
from tests.recommendation.helpers import (
    DummyProvider,
    make_dummy_recommendation,
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
)


class RecommendationThreadSafetyTests(unittest.TestCase):
    """Tests checking concurrent execution safety under thread stress."""

    THREAD_COUNT: int = 20

    def setUp(self) -> None:
        self.registry = RecommendationRegistry()
        self.engine = RecommendationEngine(registry=self.registry)
        from tests.recommendation.helpers import make_recommendation_context
        self.context = make_recommendation_context()

    def test_concurrent_recommend_calls_are_isolated(self) -> None:
        """All threads executing recommend() concurrently must succeed with independent DTO wraps."""
        rec = make_dummy_recommendation()
        self.registry.register(DummyProvider(name="PROV", priority_val=10, recommendations_to_generate=(rec,)))

        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = self.engine.recommend(self.context)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for r in results:
            self.assertIsInstance(r, RecommendationResult)
            self.assertEqual(1, len(r.recommendations))

        # Check unique identities of the returned result DTOs
        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))


if __name__ == "__main__":
    unittest.main()
