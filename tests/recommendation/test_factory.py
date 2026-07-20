"""Tests for RecommendationFactory.

Purpose:
    Verify factory constructs and configures a default RecommendationEngine.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.engine import RecommendationEngine


class RecommendationFactoryTests(unittest.TestCase):
    """Test suite validating factory instantiation methods."""

    def test_factory_returns_recommendation_engine(self) -> None:
        """create_default_recommendation_engine() must return a configured RecommendationEngine."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertIsInstance(engine, RecommendationEngine)
        self.assertEqual(5, engine.registry.provider_count)


if __name__ == "__main__":
    unittest.main()
