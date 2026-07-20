"""Tests for RecommendationEngine.

Purpose:
    Verify recommendation pipeline execution lifecycle (validation, execution order,
    statistics collation, result wrapping, metadata construction).
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.models import RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.exceptions import (
    RecommendationValidationError,
    RecommendationProviderError,
    RecommendationError,
)

from tests.recommendation.helpers import (
    DummyProvider,
    make_dummy_recommendation,
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
    make_recommendation_context,
)


class RecommendationEngineTests(unittest.TestCase):
    """Test suite validating RecommendationEngine behavior."""

    def setUp(self) -> None:
        self.registry = RecommendationRegistry()
        self.engine = RecommendationEngine(registry=self.registry)
        self.context = make_recommendation_context()

    def test_recommend_returns_recommendation_result_dto(self) -> None:
        """recommend() must return a valid RecommendationResult wrapper DTO."""
        res = self.engine.recommend(self.context)
        self.assertIsInstance(res, RecommendationResult)

    def test_default_recommend_has_empty_recommendations(self) -> None:
        """An engine with no registered providers must return empty recommendations."""
        res = self.engine.recommend(self.context)
        self.assertEqual(0, len(res.recommendations))

    def test_recommend_coordinates_providers_in_priority_order(self) -> None:
        """Providers must execute in deterministic priority order, and outputs must merge."""
        rec1 = make_dummy_recommendation(rec_id="REC_A", priority=1)
        rec2 = make_dummy_recommendation(rec_id="REC_B", priority=2)

        provider_low_prio = DummyProvider(
            name="LOW_PRIO", priority_val=100, recommendations_to_generate=(rec2,)
        )
        provider_high_prio = DummyProvider(
            name="HIGH_PRIO", priority_val=10, recommendations_to_generate=(rec1,)
        )

        self.registry.register(provider_low_prio)
        self.registry.register(provider_high_prio)

        res = self.engine.recommend(self.context)

        # Output list must preserve execution order (high priority first)
        self.assertEqual(2, len(res.recommendations))
        self.assertEqual("REC_A", res.recommendations[0].recommendation_id)
        self.assertEqual("REC_B", res.recommendations[1].recommendation_id)

        self.assertEqual(1, provider_low_prio.generate_called)
        self.assertEqual(1, provider_high_prio.generate_called)

    def test_null_inputs_raise_validation_error(self) -> None:
        """Passing None or partially missing context must raise RecommendationValidationError."""
        with self.assertRaises(RecommendationValidationError):
            self.engine.recommend(None)  # type: ignore[arg-type]

        bad_context_1 = RecommendationContext(
            match_collection=None,  # type: ignore[arg-type]
            score_result=make_mock_score_result(),
            explainability_result=make_mock_explainability_result(make_mock_score_result()),
        )
        with self.assertRaises(RecommendationValidationError):
            self.engine.recommend(bad_context_1)

    def test_provider_validation_failure_raises_provider_error(self) -> None:
        """If a provider's validate() method fails, raise RecommendationProviderError."""
        fail_provider = DummyProvider(name="FAIL_PROV", should_fail_validation=True)
        self.registry.register(fail_provider)

        with self.assertRaises(RecommendationProviderError):
            self.engine.recommend(self.context)

    def test_provider_unexpected_generate_failure_raises_recommendation_error(self) -> None:
        """If a provider raises an unexpected error, raise RecommendationError."""
        bad_provider = DummyProvider(name="BAD_PROV", should_fail_generate=True)
        self.registry.register(bad_provider)

        with self.assertRaises(RecommendationError):
            self.engine.recommend(self.context)

    def test_telemetry_and_metadata_populated(self) -> None:
        """Returned DTO must contain correct pipeline metadata and statistics."""
        res = self.engine.recommend(self.context)
        self.assertIsNotNone(res.statistics)
        self.assertIn("execution_time_ms", res.statistics)
        self.assertTrue(res.statistics["success"])

        self.assertIsNotNone(res.metadata)
        self.assertEqual("1.0.0", res.metadata["recommendation_version"])
        self.assertEqual("1.0.0", res.metadata["framework_version"])


if __name__ == "__main__":
    unittest.main()
