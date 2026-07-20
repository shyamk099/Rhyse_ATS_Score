"""Tests for PrioritizationEngine Factory integration.

Purpose:
    Verify factory configures the default engine with the PrioritizationEngine.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine


class PrioritizationProviderFactoryTests(unittest.TestCase):
    """Test suite validating factory integration."""

    def test_factory_includes_prioritization_engine(self) -> None:
        """create_default_recommendation_engine() must include PrioritizationEngine in post_processors list by default."""
        engine = RecommendationFactory.create_default_recommendation_engine()
        self.assertEqual(3, len(engine.post_processors))
        self.assertIsInstance(engine.post_processors[0], PrioritizationEngine)


if __name__ == "__main__":
    unittest.main()
