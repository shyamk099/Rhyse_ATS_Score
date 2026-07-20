"""Tests for ProjectRecommendationBuilder.

Purpose:
    Verify deterministic ID generation and field mappings in Project builder.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.project_builder import ProjectRecommendationBuilder
from ats_engine.domain.recommendation.models import Recommendation


class ProjectRecommendationBuilderTests(unittest.TestCase):
    """Test suite validating builder mappings."""

    def test_build_missing_project(self) -> None:
        """Must correctly construct missing project recommendation with clean deterministic IDs."""
        rec = ProjectRecommendationBuilder.build_missing_recommendation("Microservices")
        self.assertEqual("PROJ_MISSING_MICROSERVICES", rec.recommendation_id)
        self.assertEqual("Microservices project is missing", rec.title)
        self.assertEqual("PROJECT_MISSING", rec.category)

    def test_build_partial_project(self) -> None:
        """Must correctly construct partial project recommendation DTO."""
        rec = ProjectRecommendationBuilder.build_partial_recommendation("Event Driven")
        self.assertEqual("PROJ_PARTIAL_EVENT_DRIVEN", rec.recommendation_id)
        self.assertEqual("Expand Event Driven project details", rec.title)
        self.assertEqual("PROJECT_PARTIAL_MATCH", rec.category)

    def test_build_related_gap(self) -> None:
        """Must correctly construct related gap project recommendation DTO."""
        rec = ProjectRecommendationBuilder.build_related_gap_recommendation("Cloud Native")
        self.assertEqual("PROJ_RELATED_CLOUD_NATIVE", rec.recommendation_id)
        self.assertEqual("Add related Cloud Native project", rec.title)
        self.assertEqual("PROJECT_RELATED_GAP", rec.category)


if __name__ == "__main__":
    unittest.main()
