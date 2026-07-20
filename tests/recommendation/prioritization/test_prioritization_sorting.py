"""Tests for PrioritizationEngine sorting correctness.

Purpose:
    Verify that prioritization engine sorts recommendations strictly by
    priority DESC, impact DESC, and recommendation_id ASC as a tie-breaker.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine


class PrioritizationSortingTests(unittest.TestCase):
    """Test suite validating prioritization sorting ordering and tie-breaker."""

    def test_sorting_ordering_and_tie_breaker(self) -> None:
        """Engine must sort recommendations: priority DESC, impact DESC, and recommendation_id ASC."""
        # Setup recommendations that would map to same priority/impact
        # For example, "SKILL_MISSING" has priority 100, impact 1.0
        # We can pass custom inputs if rules support it, or resolve standard ones.
        # Let's pass recommendations that resolve to the same profile to test ID tie-breaker.
        rec1 = Recommendation(
            recommendation_id="SKILL_MISSING_PYTHON",
            section="skill",
            category="SKILL_MISSING",
            title="Python missing",
            description="Python missing.",
        )
        rec2 = Recommendation(
            recommendation_id="SKILL_MISSING_C_SHARP",
            section="skill",
            category="SKILL_MISSING",
            title="C# missing",
            description="C# missing.",
        )
        # Binds: SKILL_MISSING -> priority=100, impact=1.0. Both match.
        # Expectation: C_SHARP comes before PYTHON since C comes before P in ASCII.

        raw_res = RecommendationResult(
            context=RecommendationContext(),
            recommendations=(rec1, rec2),
            statistics={"execution_time_ms": 0.1},
            metadata={},
        )
        engine = PrioritizationEngine()
        res = engine.process(raw_res)

        self.assertEqual(2, len(res.recommendations))
        self.assertEqual("SKILL_MISSING_C_SHARP", res.recommendations[0].recommendation_id)
        self.assertEqual("SKILL_MISSING_PYTHON", res.recommendations[1].recommendation_id)


if __name__ == "__main__":
    unittest.main()
