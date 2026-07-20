"""Tests for ProjectRecommendationValidator.

Purpose:
    Verify validator catches duplicate IDs, invalid project categories, and section mismatch.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.project_validator import ProjectRecommendationValidator
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class ProjectRecommendationValidatorTests(unittest.TestCase):
    """Test suite validating ProjectRecommendationValidator."""

    def test_valid_recommendations_pass(self) -> None:
        """A list of valid, unique project recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="PROJ_MISSING_MICROSERVICES",
                section="project",
                category="PROJECT_MISSING",
                title="Microservices project missing",
                description="Microservices project required.",
            ),
            Recommendation(
                recommendation_id="PROJ_PARTIAL_KAFKA",
                section="project",
                category="PROJECT_PARTIAL_MATCH",
                title="Expand Kafka details",
                description="Kafka project partial.",
            ),
        ]
        ProjectRecommendationValidator.validate(recs)

    def test_invalid_category_raises_validation_error(self) -> None:
        """Recommendation with an invalid category for project must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="PROJ_MISSING_MICROSERVICES",
                section="project",
                category="SKILL_MISSING",  # invalid for project provider
                title="Microservices is missing",
                description="Microservices required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            ProjectRecommendationValidator.validate(recs)

    def test_duplicate_ids_raise_validation_error(self) -> None:
        """Recommendations sharing duplicate ID must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="PROJ_DUPE",
                section="project",
                category="PROJECT_MISSING",
                title="Microservices project missing",
                description="Microservices required.",
            ),
            Recommendation(
                recommendation_id="PROJ_DUPE",
                section="project",
                category="PROJECT_PARTIAL_MATCH",
                title="Expand details",
                description="Kafka partial.",
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            ProjectRecommendationValidator.validate(recs)

    def test_invalid_section_raises_validation_error(self) -> None:
        """Recommendation with non-project section must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="PROJ_MISSING_MICROSERVICES",
                section="skill",  # Invalid section for project validator
                category="PROJECT_MISSING",
                title="Microservices missing",
                description="Microservices required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            ProjectRecommendationValidator.validate(recs)


if __name__ == "__main__":
    unittest.main()
