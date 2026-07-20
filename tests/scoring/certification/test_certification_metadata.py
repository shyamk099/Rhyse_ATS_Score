"""Unit tests for the metadata of the CertificationScorer.

Purpose:
    Verify that metadata has correct keys and engine version.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.certification.scorer import CertificationScorer


class CertificationMetadataTests(unittest.TestCase):
    """Test suite validating CertificationScorer metadata fields."""

    def test_metadata_keys(self) -> None:
        scorer = CertificationScorer()
        meta = scorer.metadata()

        self.assertIn("engine_version", meta)
        self.assertIn("rules_version", meta)
        self.assertIn("pipeline_version", meta)
        self.assertEqual("1.0.0", meta["engine_version"])
