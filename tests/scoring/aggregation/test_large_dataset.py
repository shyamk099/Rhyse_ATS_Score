"""Tests for large dataset score aggregation.

Purpose:
    Verify the aggregator can handle repeated aggregations or large scale execution
    without exceeding the latency target (100ms budget).
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from tests.scoring.aggregation.helpers import make_score_result


class LargeDatasetAggregationTests(unittest.TestCase):
    """Tests verifying aggregation performance and latency bounds."""

    ITERATIONS: int = 1000

    def test_large_number_of_aggregations_latency(self) -> None:
        """Running 1000 aggregations sequentially must be fast (< 100ms total)."""
        aggregator = ScoringFactory.create_default_aggregator()
        score_result = make_score_result()

        start = time.perf_counter()
        for _ in range(self.ITERATIONS):
            aggregator.aggregate(score_result)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        # Verify that 1000 lightweight math aggregations are completed in under 100ms
        self.assertLess(
            elapsed_ms,
            100.0,
            f"Aggregation latency target exceeded: 1000 runs took {elapsed_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
