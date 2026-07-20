"""Tests for RecommendationMetadataBuilder.

Purpose:
    Verify metadata is correctly constructed with required fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.metadata_builder import RecommendationMetadataBuilder


class RecommendationMetadataTests(unittest.TestCase):
    """Test suite validating metadata builder."""

    def test_metadata_fields(self) -> None:
        """Verify built metadata dict contains the correct version and timestamp keys."""
        meta = RecommendationMetadataBuilder.build(
            recommendation_version="1.0.0",
            framework_version="1.0.0",
            pipeline_version="1.0.0",
        )
        self.assertEqual("1.0.0", meta["recommendation_version"])
        self.assertEqual("1.0.0", meta["framework_version"])
        self.assertEqual("1.0.0", meta["pipeline_version"])
        self.assertIn("timestamp", meta)
        self.assertIn("Z", meta["timestamp"])


if __name__ == "__main__":
    unittest.main()
