"""Integration tests for large resume feature collections.

Purpose:
    Verify that the pipeline successfully aggregates and matches large datasets
    (e.g., 500 skills, 100 certs, 100 projects, 50 educations, 100 experiences)
    without crashing or memory exhaustion.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class LargeResumeTests(unittest.TestCase):
    """Large scale dataset matching tests."""

    def setUp(self) -> None:
        """Load large scale feature collections."""
        res_path = Path("tests/fixtures/resume_large.json")
        job_path = Path("tests/fixtures/job_large.json")

        self.assertTrue(res_path.is_file())
        self.assertTrue(job_path.is_file())

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_large_resume_matching_execution(self) -> None:
        """Pipeline scales to match large datasets (900 total features) correctly."""
        skill_col = self._match_service.match(self._resume_features, self._job_features, ["skill"])
        exp_col = self._match_service.match(self._resume_features, self._job_features, ["experience"])
        edu_col = self._match_service.match(self._resume_features, self._job_features, ["education"])
        proj_col = self._match_service.match(self._resume_features, self._job_features, ["project"])
        cert_col = self._match_service.match(self._resume_features, self._job_features, ["certification"])

        res = self._canonical_match_service.build(
            skill_matches=skill_col,
            experience_matches=exp_col,
            education_matches=edu_col,
            project_matches=proj_col,
            certification_matches=cert_col,
        )

        self.assertIsNotNone(res)
        # All 900 features should match 1:1 since inputs are identical
        self.assertEqual(850, len(res.results)) # 500 skills + 100 exp + 50 edu + 100 proj + 100 cert
        self.assertEqual(0, res.validation_summary.total_errors)
