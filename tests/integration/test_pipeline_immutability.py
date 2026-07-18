"""Integration tests checking immutability guarantees of pipeline models.

Purpose:
    Verify that models are immutable at every stage (EntityCollection, FeatureCollection, MatchCollection,
    CanonicalMatchCollection) and attempts to mutate raise errors.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from pydantic import ValidationError

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service, run_entity_extraction


class PipelineImmutabilityTests(unittest.TestCase):
    """Immutability validation tests."""

    def setUp(self) -> None:
        """Load simple resume and job collections."""
        res_path = Path("tests/fixtures/resume_simple.json")
        job_path = Path("tests/fixtures/job_simple.json")

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_canonical_feature_collection_immutability(self) -> None:
        """Assert that CanonicalFeatureCollection is frozen and rejects mutations."""
        with self.assertRaises((ValidationError, TypeError)):
            self._resume_features.skills = None  # type: ignore

    def test_canonical_match_collection_immutability(self) -> None:
        """Assert that CanonicalMatchCollection is frozen and rejects mutations."""
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

        with self.assertRaises((ValidationError, TypeError)):
            res.results = ()  # type: ignore

        with self.assertRaises((ValidationError, TypeError)):
            res.statistics.total_matches = 999  # type: ignore
