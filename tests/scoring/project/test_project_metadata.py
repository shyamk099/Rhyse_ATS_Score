"""Unit tests for the metadata of the ProjectScorer.

Purpose:
    Verify that metadata has correct keys and engine version.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.project.scorer import ProjectScorer


class ProjectMetadataTests(unittest.TestCase):
    """Test suite validating ProjectScorer metadata fields."""

    def test_metadata_keys(self) -> None:
        scorer = ProjectScorer()
        meta = scorer.metadata()

        self.assertIn("engine_version", meta)
        self.assertIn("rules_version", meta)
        self.assertIn("pipeline_version", meta)
        self.assertEqual("1.0.0", meta["engine_version"])
