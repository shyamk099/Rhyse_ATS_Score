"""Integration tests validating pipeline execution determinism.

Purpose:
    Execute the matching pipeline repeatedly, serialize results, hash them,
    and assert that they are 100% identical.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class PipelineDeterminismTests(unittest.TestCase):
    """Determinism verification tests."""

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

    def test_pipeline_execution_determinism(self) -> None:
        """Pipeline execution 100 times returns identical hashes (determinism check)."""
        hashes = set()
        rules = {"correlation_id": "fixed-corr-id"}
        
        for _ in range(100):
            skill_col = self._match_service.match(self._resume_features, self._job_features, ["skill"], rules=rules)
            exp_col = self._match_service.match(self._resume_features, self._job_features, ["experience"], rules=rules)
            edu_col = self._match_service.match(self._resume_features, self._job_features, ["education"], rules=rules)
            proj_col = self._match_service.match(self._resume_features, self._job_features, ["project"], rules=rules)
            cert_col = self._match_service.match(self._resume_features, self._job_features, ["certification"], rules=rules)

            res = self._canonical_match_service.build(
                skill_matches=skill_col,
                experience_matches=exp_col,
                education_matches=edu_col,
                project_matches=proj_col,
                certification_matches=cert_col,
            )

            # Dump to JSON to serialize
            data = res.model_dump_json()
            
            # Since execution_timestamp changes, we must ignore/override it to check structural determinism
            data_dict = json.loads(data)
            for r in data_dict["results"]:
                r["metadata"]["execution_timestamp"] = "2026-07-13T20:00:00Z"
            data_dict["statistics"]["execution_duration_ms"] = 0.0

            normalized_json = json.dumps(data_dict, sort_keys=True)
            sha = hashlib.sha256(normalized_json.encode("utf-8")).hexdigest()
            hashes.add(sha)

        self.assertEqual(1, len(hashes), f"Non-deterministic pipeline output detected! Generated {len(hashes)} different hashes: {hashes}")

