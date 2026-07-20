"""Tests for RecommendationOrchestrationValidator.

Purpose:
    Verify validator asserts conservation, duplicates, and sorting order.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.orchestration.orchestration_validator import RecommendationOrchestrationValidator
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class OrchestrationValidatorTests(unittest.TestCase):
    """Test suite validating RecommendationOrchestrationValidator constraints."""

    def setUp(self) -> None:
        self.rec1 = Recommendation(
            recommendation_id="SKILL_MISSING_PYTHON",
            section="skill",
            category="SKILL_MISSING",
            title="Python missing",
            description="Python missing.",
            priority=100,
            impact=1.0,
            confidence=1.0,
        )
        self.rec2 = Recommendation(
            recommendation_id="PROJ_MISSING_KAFKA",
            section="project",
            category="PROJECT_MISSING",
            title="Kafka project missing",
            description="Kafka project missing.",
            priority=80,
            impact=0.75,
            confidence=1.0,
        )
        self.recs = (self.rec1, self.rec2)

    def test_valid_mappings_pass(self) -> None:
        """A valid grouping configuration must pass validation successfully."""
        by_sec = {"skill": (self.rec1,), "project": (self.rec2,)}
        by_cat = {"SKILL_MISSING": (self.rec1,), "PROJECT_MISSING": (self.rec2,)}
        by_pri = {"High": (self.rec1,), "Medium": (self.rec2,), "Low": ()}

        RecommendationOrchestrationValidator.validate(
            recommendations=self.recs,
            by_section=by_sec,
            by_category=by_cat,
            by_priority=by_pri,
        )

    def test_conservation_mismatch_raises_validation_error(self) -> None:
        """If grouping sums don't match total count, must raise RecommendationValidationError."""
        by_sec = {"skill": (self.rec1,)}  # Missing self.rec2
        by_cat = {"SKILL_MISSING": (self.rec1,), "PROJECT_MISSING": (self.rec2,)}
        by_pri = {"High": (self.rec1,), "Medium": (self.rec2,), "Low": ()}

        with self.assertRaises(RecommendationValidationError):
            RecommendationOrchestrationValidator.validate(
                recommendations=self.recs,
                by_section=by_sec,
                by_category=by_cat,
                by_priority=by_pri,
            )

    def test_sorting_sequence_mismatch_raises_validation_error(self) -> None:
        """If recommendations inside group are out of order, must raise RecommendationValidationError."""
        # Main list: rec1, rec2
        # Group list: rec2, rec1 (reverse order)
        by_sec = {"combined": (self.rec2, self.rec1)}
        by_cat = {"combined": (self.rec2, self.rec1)}
        by_pri = {"combined": (self.rec2, self.rec1)}

        with self.assertRaises(RecommendationValidationError):
            RecommendationOrchestrationValidator.validate(
                recommendations=self.recs,
                by_section=by_sec,
                by_category=by_cat,
                by_priority=by_pri,
            )


if __name__ == "__main__":
    unittest.main()
