"""Integration tests for large job description feature collections.

Purpose:
    Verify that the pipeline successfully scales matching against large job description feature sets
    without performance degradations or memory issues.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class LargeJobDescriptionTests(unittest.TestCase):
    """Large scale job description matching tests."""

    def setUp(self) -> None:
        """Load large scale feature collections."""
        res_path = Path("tests/fixtures/resume_large.json")
        job_path = Path("tests/fixtures/job_large.json")

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_large_job_description_matching(self) -> None:
        """Pipeline handles matching against a large job description collection successfully."""
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
        self.assertEqual(850, len(res.results))
        self.assertEqual(0, res.validation_summary.total_errors)
        self.assertGreater(res.statistics.execution_duration_ms, 0.0)
