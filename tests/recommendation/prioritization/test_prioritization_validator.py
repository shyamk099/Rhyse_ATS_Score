"""Tests for PrioritizationValidator.

Purpose:
    Verify validation checks and sorting order assertion of prioritized results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.prioritization_validator import PrioritizationValidator
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class PrioritizationValidatorTests(unittest.TestCase):
    """Test suite validating PrioritizationValidator."""

    def test_valid_sorted_recommendations_pass(self) -> None:
        """A sorted list of unique prioritized recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=100,
                impact=1.0,
                confidence=1.0,
            ),
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
                priority=80,
                impact=0.75,
                confidence=1.0,
            ),
        ]
        PrioritizationValidator.validate(recs)

    def test_invalid_sorting_order_raises_validation_error(self) -> None:
        """If recommendations are not sorted by priority DESC, must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="PROJ_MISSING_KAFKA",
                section="project",
                category="PROJECT_MISSING",
                title="Kafka project missing",
                description="Kafka project missing.",
                priority=80,
                impact=0.75,
                confidence=1.0,
            ),
            Recommendation(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=100,  # Higher priority placed second
                impact=1.0,
                confidence=1.0,
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            PrioritizationValidator.validate(recs)

    def test_invalid_bounds_raises_validation_error(self) -> None:
        """If priority, impact, or confidence falls out of range, must raise RecommendationValidationError."""
        class MockRec:
            def __init__(self, recommendation_id, section, category, title, description, priority, impact, confidence):
                self.recommendation_id = recommendation_id
                self.section = section
                self.category = category
                self.title = title
                self.description = description
                self.priority = priority
                self.impact = impact
                self.confidence = confidence

        bad_priority = [
            MockRec(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=-1,  # out of bounds
                impact=1.0,
                confidence=1.0,
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            PrioritizationValidator.validate(bad_priority)

        bad_confidence = [
            MockRec(
                recommendation_id="SKILL_MISSING_PYTHON",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Python missing.",
                priority=100,
                impact=1.0,
                confidence=1.5,  # out of bounds
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            PrioritizationValidator.validate(bad_confidence)


if __name__ == "__main__":
    unittest.main()
