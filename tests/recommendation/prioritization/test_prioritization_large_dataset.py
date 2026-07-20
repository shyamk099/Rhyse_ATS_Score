"""Tests for PrioritizationEngine performance latency.

Purpose:
    Verify that processing recommendations for 1000 contexts sequentially
    completes within 100ms.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine


class PrioritizationLargeDatasetTests(unittest.TestCase):
    """Latency performance tests validating prioritization execution budget."""

    ITERATIONS: int = 1000

    def test_large_dataset_prioritization_latency(self) -> None:
        """1000 sequential process() calls must execute within a 100ms budget."""
        engine = PrioritizationEngine()

        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
            ),
        ]
        raw_result = RecommendationResult(
            context=RecommendationContext(),
            recommendations=tuple(recs),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )

        start = time.perf_counter()
        for _ in range(self.ITERATIONS):
            engine.process(raw_result)
        duration_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(
            duration_ms,
            100.0,
            f"Prioritization engine scale latency target exceeded: 1000 runs took {duration_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
