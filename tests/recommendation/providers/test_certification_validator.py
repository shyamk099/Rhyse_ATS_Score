"""Tests for CertificationRecommendationValidator.

Purpose:
    Verify validator catches duplicate IDs, invalid certification categories, and section mismatch.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.certification_validator import CertificationRecommendationValidator
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class CertificationRecommendationValidatorTests(unittest.TestCase):
    """Test suite validating CertificationRecommendationValidator."""

    def test_valid_recommendations_pass(self) -> None:
        """A list of valid, unique certification recommendations must validate successfully."""
        recs = [
            Recommendation(
                recommendation_id="CERT_MISSING_AWS_SAA",
                section="certification",
                category="CERTIFICATION_MISSING",
                title="AWS SAA missing",
                description="AWS SAA required.",
            ),
            Recommendation(
                recommendation_id="CERT_PARTIAL_AZURE",
                section="certification",
                category="CERTIFICATION_PARTIAL_MATCH",
                title="Expand Azure details",
                description="Azure certification partial.",
            ),
        ]
        CertificationRecommendationValidator.validate(recs)

    def test_invalid_category_raises_validation_error(self) -> None:
        """Recommendation with an invalid category for certification must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="CERT_MISSING_AWS_SAA",
                section="certification",
                category="SKILL_MISSING",  # invalid for certification provider
                title="AWS SAA is missing",
                description="AWS SAA required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            CertificationRecommendationValidator.validate(recs)

    def test_duplicate_ids_raise_validation_error(self) -> None:
        """Recommendations sharing duplicate ID must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="CERT_DUPE",
                section="certification",
                category="CERTIFICATION_MISSING",
                title="AWS SAA missing",
                description="AWS SAA required.",
            ),
            Recommendation(
                recommendation_id="CERT_DUPE",
                section="certification",
                category="CERTIFICATION_PARTIAL_MATCH",
                title="Expand details",
                description="Azure partial.",
            ),
        ]
        with self.assertRaises(RecommendationValidationError):
            CertificationRecommendationValidator.validate(recs)

    def test_invalid_section_raises_validation_error(self) -> None:
        """Recommendation with non-certification section must raise RecommendationValidationError."""
        recs = [
            Recommendation(
                recommendation_id="CERT_MISSING_AWS_SAA",
                section="skill",  # Invalid section for certification validator
                category="CERTIFICATION_MISSING",
                title="AWS SAA missing",
                description="AWS SAA required.",
            )
        ]
        with self.assertRaises(RecommendationValidationError):
            CertificationRecommendationValidator.validate(recs)


if __name__ == "__main__":
    unittest.main()
