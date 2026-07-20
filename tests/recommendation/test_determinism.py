"""Tests for recommendation determinism.

Purpose:
    Verify that repeated recommend() calls on the same registry/inputs
    produce identical execution order and result outputs.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from tests.recommendation.helpers import (
    DummyProvider,
    make_dummy_recommendation,
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
)


class RecommendationDeterminismTests(unittest.TestCase):
    """Tests validating deterministic recommendation order."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.registry = RecommendationRegistry()
        self.engine = RecommendationEngine(registry=self.registry)
        from tests.recommendation.helpers import make_recommendation_context
        self.context = make_recommendation_context()

    def test_recommendation_order_is_fully_deterministic(self) -> None:
        """Repeated runs with multiple providers must produce identical ordered recommendation lists."""
        rec1 = make_dummy_recommendation(rec_id="REC_A", priority=1)
        rec2 = make_dummy_recommendation(rec_id="REC_B", priority=2)

        self.registry.register(DummyProvider(name="LOW_PRIO", priority_val=100, recommendations_to_generate=(rec2,)))
        self.registry.register(DummyProvider(name="HIGH_PRIO", priority_val=10, recommendations_to_generate=(rec1,)))

        first = self.engine.recommend(self.context)
        first_ids = [r.recommendation_id for r in first.recommendations]

        for _ in range(self.REPETITIONS - 1):
            res = self.engine.recommend(self.context)
            res_ids = [r.recommendation_id for r in res.recommendations]
            self.assertEqual(first_ids, res_ids)


if __name__ == "__main__":
    unittest.main()
