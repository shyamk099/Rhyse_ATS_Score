"""Integration tests for the End-to-End pipeline.

Purpose:
    Verify that a resume file can run through parsing, entity extraction, feature engineering,
    matching engine, and canonical match collection successfully.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from tests.integration.pipeline_helpers import run_full_pipeline


class EndToEndPipelineTests(unittest.TestCase):
    """Integration test suite executing the full ingestion-to-match pipeline."""

    def setUp(self) -> None:
        """Load simple job description fixture."""
        self._resume_path = Path("samples/resume.pdf")
        self._job_fixture_path = Path("tests/fixtures/job_simple.json")

        self.assertTrue(self._resume_path.is_file())
        self.assertTrue(self._job_fixture_path.is_file())

        with open(self._job_fixture_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())
    def test_end_to_end_pipeline_success(self) -> None:
        """The full pipeline runs successfully on a valid PDF resume file."""
        rules_payload = {
            "skill_matching_rules": {"comparison_mode": "ALL"},
            "experience_matching_rules": {"comparison_mode": "ALL"},
            "education_matching_rules": {"comparison_mode": "ALL"},
            "project_matching_rules": {"comparison_mode": "ALL"},
            "certification_matching_rules": {"comparison_mode": "ALL"},
        }
        canonical_match_col = run_full_pipeline(
            resume_path=self._resume_path,
            job_features=self._job_features,
            matching_rules_payload=rules_payload,
        )

        self.assertIsNotNone(canonical_match_col)
        self.assertEqual(len(canonical_match_col.results), 0)
        self.assertEqual(0, canonical_match_col.validation_summary.total_errors)


