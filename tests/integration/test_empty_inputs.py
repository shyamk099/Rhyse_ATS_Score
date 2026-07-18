"""Integration tests validating empty and null/missing inputs.

Purpose:
    Verify that passing empty CanonicalFeatureCollections, empty MatchCollections,
    or empty/missing lists does not cause pipeline execution to crash.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class EmptyInputsTests(unittest.TestCase):
    """Empty and null matching pipeline tests."""

    def setUp(self) -> None:
        """Load empty resume and job collections."""
        res_path = Path("tests/fixtures/resume_empty.json")
        job_path = Path("tests/fixtures/job_empty.json")

        self.assertTrue(res_path.is_file())
        self.assertTrue(job_path.is_file())

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_empty_collections_produce_empty_matches_without_crashing(self) -> None:
        """Empty feature collections match successfully producing zero matches without errors."""
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
        self.assertEqual(0, len(res.results))
        self.assertEqual(0, res.statistics.total_matches)
        self.assertEqual(0, res.validation_summary.total_errors)
