"""Tests for CertificationRecommendationBuilder.

Purpose:
    Verify deterministic ID generation and field mappings in Certification builder.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.providers.certification_builder import CertificationRecommendationBuilder
from ats_engine.domain.recommendation.models import Recommendation


class CertificationRecommendationBuilderTests(unittest.TestCase):
    """Test suite validating builder mappings."""

    def test_build_missing_certification(self) -> None:
        """Must correctly construct missing certification recommendation with clean deterministic IDs."""
        rec = CertificationRecommendationBuilder.build_missing_recommendation("AWS SAA")
        self.assertEqual("CERT_MISSING_AWS_SAA", rec.recommendation_id)
        self.assertEqual("AWS SAA certification is missing", rec.title)
        self.assertEqual("CERTIFICATION_MISSING", rec.category)

    def test_build_partial_certification(self) -> None:
        """Must correctly construct partial certification recommendation DTO."""
        rec = CertificationRecommendationBuilder.build_partial_recommendation("Azure Administrator")
        self.assertEqual("CERT_PARTIAL_AZURE_ADMINISTRATOR", rec.recommendation_id)
        self.assertEqual("Expand Azure Administrator details", rec.title)
        self.assertEqual("CERTIFICATION_PARTIAL_MATCH", rec.category)

    def test_build_expired(self) -> None:
        """Must correctly construct expired certification recommendation DTO."""
        rec = CertificationRecommendationBuilder.build_expired_recommendation("PMP")
        self.assertEqual("CERT_EXPIRED_PMP", rec.recommendation_id)
        self.assertEqual("Renew PMP certification", rec.title)
        self.assertEqual("CERTIFICATION_EXPIRED", rec.category)


if __name__ == "__main__":
    unittest.main()
