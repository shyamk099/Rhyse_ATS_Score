"""Tests for aggregation metadata.

Purpose:
    Verify that aggregation-level metadata fields are correctly captured
    in last_aggregation_stats after aggregate() completes.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator

from tests.scoring.aggregation.helpers import make_score_result, make_perfect_score_result


class AggregationMetadataTests(unittest.TestCase):
    """Tests verifying aggregation metadata fields are correctly populated."""

    def setUp(self) -> None:
        self.aggregator = ScoringFactory.create_default_aggregator()

    def test_aggregation_version_in_stats(self) -> None:
        """last_aggregation_stats must contain aggregation_version."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertIn("aggregation_version", stats)
        self.assertTrue(stats["aggregation_version"])

    def test_pipeline_version_in_stats(self) -> None:
        """last_aggregation_stats must contain pipeline_version."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertIn("pipeline_version", stats)
        self.assertTrue(stats["pipeline_version"])

    def test_aggregation_time_ms_is_non_negative(self) -> None:
        """aggregation_time_ms must be >= 0 after aggregate()."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertGreaterEqual(stats["aggregation_time_ms"], 0.0)

    def test_normalization_time_ms_is_non_negative(self) -> None:
        """normalization_time_ms must be >= 0 after aggregate()."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertGreaterEqual(stats["normalization_time_ms"], 0.0)

    def test_weighting_time_ms_is_non_negative(self) -> None:
        """weighting_time_ms must be >= 0 after aggregate()."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertGreaterEqual(stats["weighting_time_ms"], 0.0)

    def test_overall_score_in_stats_matches_result(self) -> None:
        """overall_score in stats must match the returned ScoreResult.overall_score."""
        result = self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertAlmostEqual(result.overall_score, stats["overall_score"], places=6)

    def test_stats_keys_are_stable(self) -> None:
        """All expected keys must be present after every aggregate() call."""
        expected = {
            "aggregation_time_ms", "normalization_time_ms", "weighting_time_ms",
            "overall_score", "pipeline_version", "aggregation_version",
        }
        self.aggregator.aggregate(make_score_result())
        self.assertEqual(expected, set(self.aggregator.last_aggregation_stats.keys()))

    def test_stats_are_copy_not_reference(self) -> None:
        """last_aggregation_stats must return a copy, not a mutable reference."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        stats["aggregation_version"] = "tampered"
        fresh = self.aggregator.last_aggregation_stats
        self.assertNotEqual("tampered", fresh.get("aggregation_version"))

    def test_perfect_score_stats_overall_is_100(self) -> None:
        """Stats overall_score must be 100.0 for a perfect resume."""
        self.aggregator.aggregate(make_perfect_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertAlmostEqual(100.0, stats["overall_score"], places=6)


if __name__ == "__main__":
    unittest.main()
