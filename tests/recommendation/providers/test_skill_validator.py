"""Tests for SkillRecommendationValidator.

Purpose:
    Verify validator catches duplicates, empty strings, and invalid categories.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.skill_validator import SkillRecommendationValidator
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class SkillRecommendationValidatorTests(unittest.TestCase):
    """Test suite validating SkillRecommendationValidator."""

    def test_valid_recommendations_pass(self) -> None:
        """A list of valid, unique skill recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="REC-SKILL-MISSING-1",
                section="skill",
                category="SKILL_MISSING",
                title="Python is missing",
                description="Python required.",
            ),
            Recommendation(
                recommendation_id="REC-SKILL-PARTIAL-2",
                section="skill",
                category="SKILL_PARTIAL_MATCH",
                title="Expand Docker experience",
                description="Docker partial.",
            ),
        ]
        SkillRecommendationValidator.validate(recs)

    def test_empty_title_raises_validation_error(self) -> None:
        """Recommendation with an empty title must raise ValidationError at instantiation."""
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            Recommendation(
                recommendation_id="REC-1",
                section="skill",
                category="SKILL_MISSING",
                title="",
                description="Desc",
            )

    def test_empty_description_raises_validation_error(self) -> None:
        """Recommendation with an empty description must raise ValidationError at instantiation."""
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            Recommendation(
                recommendation_id="REC-1",
                section="skill",
                category="SKILL_MISSING",
                title="Title",
                description="",
            )

    def test_invalid_category_raises_validation_error(self) -> None:
        """Recommendation with a non-skill category must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="REC-1",
                section="skill",
                category="EXPERIENCE_MISSING",  # invalid for skill provider
                title="Title",
                description="Desc",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            SkillRecommendationValidator.validate(recs)

    def test_duplicate_ids_raise_validation_error(self) -> None:
        """Recommendations sharing duplicate ID must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="REC-DUPE",
                section="skill",
                category="SKILL_MISSING",
                title="Python missing",
                description="Desc 1",
            ),
            Recommendation(
                recommendation_id="REC-DUPE",
                section="skill",
                category="SKILL_PARTIAL_MATCH",
                title="Docker partial",
                description="Desc 2",
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            SkillRecommendationValidator.validate(recs)


if __name__ == "__main__":
    unittest.main()
