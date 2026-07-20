"""Tests for PrioritizationEngine determinism.

Purpose:
    Verify repeated prioritization process runs yield identical output.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine


class PrioritizationDeterminismTests(unittest.TestCase):
    """Test suite validating prioritization output determinism."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.engine = PrioritizationEngine()
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
        self.raw_result = RecommendationResult(
            context=RecommendationContext(),
            recommendations=tuple(recs),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )

    def test_processing_is_fully_deterministic(self) -> None:
        """Repeated engine.process() calls must yield identical prioritized lists."""
        first = self.engine.process(self.raw_result)
        first_ids = [r.recommendation_id for r in first.recommendations]

        for _ in range(self.REPETITIONS - 1):
            res = self.engine.process(self.raw_result)
            res_ids = [r.recommendation_id for r in res.recommendations]
            self.assertEqual(first_ids, res_ids)


if __name__ == "__main__":
    unittest.main()
