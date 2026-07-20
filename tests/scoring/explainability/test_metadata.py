"""Tests for ExplainabilityMetadataBuilder.

Purpose:
    Verify metadata is correctly constructed with required fields.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.metadata_builder import ExplainabilityMetadataBuilder


class ExplainabilityMetadataTests(unittest.TestCase):
    """Test suite validating explainability metadata builder."""

    def test_metadata_fields(self) -> None:
        """Verify built metadata dict contains the correct version and timestamp keys."""
        meta = ExplainabilityMetadataBuilder.build(
            explainability_version="1.0.0",
            pipeline_version="1.0.0",
            framework_version="1.0.0",
        )
        self.assertEqual("1.0.0", meta["explainability_version"])
        self.assertEqual("1.0.0", meta["pipeline_version"])
        self.assertEqual("1.0.0", meta["framework_version"])
        self.assertIn("timestamp", meta)
        self.assertIn("T", meta["timestamp"])


if __name__ == "__main__":
    unittest.main()
