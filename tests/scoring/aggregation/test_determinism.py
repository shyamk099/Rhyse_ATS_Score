"""Tests for aggregation determinism.

Purpose:
    Verify that repeated aggregate() calls on the same ScoreResult
    produce identical overall_score values and consistent statistics keys.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
from ats_engine.domain.ats_scoring.aggregation.normalization import ScoreNormalizer

from tests.scoring.aggregation.helpers import make_score_result, make_perfect_score_result, make_zero_score_result


class AggregationDeterminismTests(unittest.TestCase):
    """Tests verifying repeated aggregation produces identical results."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.aggregator = OverallScoreAggregator()
        self.score_result = make_score_result()

    def test_overall_score_identical_across_repetitions(self) -> None:
        """Repeated aggregate() calls must produce the same overall_score."""
        first = self.aggregator.aggregate(self.score_result).overall_score
        for _ in range(self.REPETITIONS - 1):
            result = self.aggregator.aggregate(self.score_result)
            self.assertAlmostEqual(first, result.overall_score, places=10)

    def test_perfect_score_always_100(self) -> None:
        """Perfect resume must always yield exactly 100.0."""
        for _ in range(self.REPETITIONS):
            result = self.aggregator.aggregate(make_perfect_score_result())
            self.assertAlmostEqual(100.0, result.overall_score, places=10)

    def test_zero_score_always_zero(self) -> None:
        """Zero resume must always yield exactly 0.0."""
        for _ in range(self.REPETITIONS):
            result = self.aggregator.aggregate(make_zero_score_result())
            self.assertAlmostEqual(0.0, result.overall_score, places=10)

    def test_stats_keys_stable_across_repetitions(self) -> None:
        """Statistics keys must be identical on every call."""
        self.aggregator.aggregate(self.score_result)
        first_keys = set(self.aggregator.last_aggregation_stats.keys())
        for _ in range(self.REPETITIONS - 1):
            self.aggregator.aggregate(self.score_result)
            self.assertEqual(first_keys, set(self.aggregator.last_aggregation_stats.keys()))

    def test_normalize_all_is_deterministic(self) -> None:
        """ScoreNormalizer.normalize_all() must return identical values each call."""
        first = ScoreNormalizer.normalize_all(self.score_result)
        for _ in range(self.REPETITIONS - 1):
            normalized = ScoreNormalizer.normalize_all(self.score_result)
            for section, value in first.items():
                self.assertAlmostEqual(value, normalized[section], places=10)

    def test_original_not_mutated_across_repetitions(self) -> None:
        """Input ScoreResult must remain with overall_score=None after many calls."""
        for _ in range(self.REPETITIONS):
            self.aggregator.aggregate(self.score_result)
        self.assertIsNone(self.score_result.overall_score)


if __name__ == "__main__":
    unittest.main()
