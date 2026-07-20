"""Tests for AggregationStatisticsBuilder.

Purpose:
    Verify that the statistics builder produces correct keys, types,
    rounding, and handles edge cases.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.statistics_builder import AggregationStatisticsBuilder


class AggregationStatisticsBuilderTests(unittest.TestCase):
    """Tests for AggregationStatisticsBuilder.build()."""

    def test_returns_dict(self) -> None:
        """build() must return a plain dict."""
        result = AggregationStatisticsBuilder.build()
        self.assertIsInstance(result, dict)

    def test_required_keys_present(self) -> None:
        """All required keys must be present in the output."""
        result = AggregationStatisticsBuilder.build()
        expected_keys = {
            "aggregation_time_ms",
            "normalization_time_ms",
            "weighting_time_ms",
            "overall_score",
            "pipeline_version",
            "aggregation_version",
        }
        self.assertEqual(expected_keys, set(result.keys()))

    def test_default_values(self) -> None:
        """Default build must produce sensible zero-state values."""
        result = AggregationStatisticsBuilder.build()
        self.assertEqual(0.0, result["aggregation_time_ms"])
        self.assertEqual(0.0, result["normalization_time_ms"])
        self.assertEqual(0.0, result["weighting_time_ms"])
        self.assertIsNone(result["overall_score"])
        self.assertEqual("1.0.0", result["pipeline_version"])
        self.assertEqual("1.0.0", result["aggregation_version"])

    def test_aggregation_time_rounded(self) -> None:
        """aggregation_time_ms must be rounded to 4 decimal places."""
        result = AggregationStatisticsBuilder.build(aggregation_time_ms=5.123456789)
        self.assertEqual(round(5.123456789, 4), result["aggregation_time_ms"])

    def test_normalization_time_rounded(self) -> None:
        """normalization_time_ms must be rounded to 4 decimal places."""
        result = AggregationStatisticsBuilder.build(normalization_time_ms=3.987654321)
        self.assertEqual(round(3.987654321, 4), result["normalization_time_ms"])

    def test_weighting_time_rounded(self) -> None:
        """weighting_time_ms must be rounded to 4 decimal places."""
        result = AggregationStatisticsBuilder.build(weighting_time_ms=1.111111111)
        self.assertEqual(round(1.111111111, 4), result["weighting_time_ms"])

    def test_overall_score_stored(self) -> None:
        """overall_score must be stored as provided."""
        result = AggregationStatisticsBuilder.build(overall_score=87.5)
        self.assertAlmostEqual(87.5, result["overall_score"], places=6)

    def test_overall_score_none_stored(self) -> None:
        """overall_score=None must be stored as None."""
        result = AggregationStatisticsBuilder.build(overall_score=None)
        self.assertIsNone(result["overall_score"])

    def test_custom_versions_stored(self) -> None:
        """Custom pipeline_version and aggregation_version must be stored."""
        result = AggregationStatisticsBuilder.build(
            pipeline_version="2.0.0",
            aggregation_version="3.1.0",
        )
        self.assertEqual("2.0.0", result["pipeline_version"])
        self.assertEqual("3.1.0", result["aggregation_version"])

    def test_zero_times_stored(self) -> None:
        """Zero timing values must be stored as 0.0."""
        result = AggregationStatisticsBuilder.build(
            aggregation_time_ms=0.0,
            normalization_time_ms=0.0,
            weighting_time_ms=0.0,
        )
        self.assertEqual(0.0, result["aggregation_time_ms"])
        self.assertEqual(0.0, result["normalization_time_ms"])
        self.assertEqual(0.0, result["weighting_time_ms"])


if __name__ == "__main__":
    unittest.main()
