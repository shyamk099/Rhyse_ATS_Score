"""Tests for ScoringFactory.create_default_aggregator().

Purpose:
    Verify factory produces a correctly wired OverallScoreAggregator
    with default and custom weight configurations.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult

from tests.scoring.aggregation.helpers import make_score_result, make_perfect_score_result


class AggregatorFactoryTests(unittest.TestCase):
    """Tests for ScoringFactory.create_default_aggregator()."""

    def test_factory_returns_overall_score_aggregator(self) -> None:
        """create_default_aggregator() must return an OverallScoreAggregator."""
        agg = ScoringFactory.create_default_aggregator()
        self.assertIsInstance(agg, OverallScoreAggregator)

    def test_factory_aggregator_has_weight_config(self) -> None:
        """Returned aggregator must have a SectionWeightConfiguration."""
        agg = ScoringFactory.create_default_aggregator()
        self.assertIsInstance(agg.weight_config, SectionWeightConfiguration)

    def test_factory_default_weights_are_standard(self) -> None:
        """Factory default aggregator must use standard weights."""
        agg = ScoringFactory.create_default_aggregator()
        self.assertAlmostEqual(0.35, agg.weight_config.skill, places=9)
        self.assertAlmostEqual(0.30, agg.weight_config.experience, places=9)
        self.assertAlmostEqual(0.15, agg.weight_config.education, places=9)
        self.assertAlmostEqual(0.10, agg.weight_config.project, places=9)
        self.assertAlmostEqual(0.10, agg.weight_config.certification, places=9)

    def test_factory_aggregator_can_aggregate(self) -> None:
        """Factory aggregator must successfully aggregate a valid ScoreResult."""
        agg = ScoringFactory.create_default_aggregator()
        result = agg.aggregate(make_score_result())
        self.assertIsInstance(result, ScoreResult)
        self.assertIsNotNone(result.overall_score)

    def test_factory_with_custom_weight_config(self) -> None:
        """create_default_aggregator() must accept a custom weight configuration."""
        custom = SectionWeightConfiguration(
            skill=0.50, experience=0.20, education=0.10,
            project=0.10, certification=0.10,
        )
        agg = ScoringFactory.create_default_aggregator(weight_config=custom)
        self.assertAlmostEqual(0.50, agg.weight_config.skill, places=9)

    def test_factory_with_none_weight_config_uses_default(self) -> None:
        """create_default_aggregator(None) must fall back to default weights."""
        agg = ScoringFactory.create_default_aggregator(weight_config=None)
        self.assertAlmostEqual(0.35, agg.weight_config.skill, places=9)

    def test_factory_perfect_score_yields_100(self) -> None:
        """Factory aggregator must yield 100.0 for a perfect ScoreResult."""
        agg = ScoringFactory.create_default_aggregator()
        result = agg.aggregate(make_perfect_score_result())
        self.assertAlmostEqual(100.0, result.overall_score, places=6)

    def test_factory_create_default_aggregator_is_callable(self) -> None:
        """ScoringFactory.create_default_aggregator must be a static callable."""
        self.assertTrue(callable(ScoringFactory.create_default_aggregator))


if __name__ == "__main__":
    unittest.main()
