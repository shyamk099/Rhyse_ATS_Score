"""Tests for thread-safe concurrent score aggregation.

Purpose:
    Verify that multiple threads can invoke OverallScoreAggregator.aggregate()
    concurrently on the same or different ScoreResult objects and each
    receives an independent, correct, and isolated aggregated result.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult

from tests.scoring.aggregation.helpers import make_score_result


class AggregatorThreadSafetyTests(unittest.TestCase):
    """Tests verifying OverallScoreAggregator is safe for concurrent use."""

    THREAD_COUNT: int = 20

    def test_concurrent_aggregations_produce_valid_results(self) -> None:
        """All threads must receive a valid ScoreResult with no exceptions."""
        aggregator = ScoringFactory.create_default_aggregator()
        score_result = make_score_result()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = aggregator.aggregate(score_result)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for result in results:
            self.assertIsInstance(result, ScoreResult)
            self.assertIsNotNone(result.overall_score)

    def test_concurrent_results_are_independent(self) -> None:
        """Results from concurrent threads must not share same object references."""
        aggregator = ScoringFactory.create_default_aggregator()
        score_result = make_score_result()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = aggregator.aggregate(score_result)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors))
        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))

    def test_concurrent_last_aggregation_stats_copy_is_safe(self) -> None:
        """last_aggregation_stats must not cause race conditions or corrupt state."""
        aggregator = ScoringFactory.create_default_aggregator()
        score_result = make_score_result()
        errors: list[Exception] = []

        def run() -> None:
            try:
                aggregator.aggregate(score_result)
                stats = aggregator.last_aggregation_stats
                self.assertIsNotNone(stats.get("overall_score"))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run) for _ in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")


if __name__ == "__main__":
    unittest.main()
