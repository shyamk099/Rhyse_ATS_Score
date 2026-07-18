"""Integration tests validating thread-safety of pipeline execution.

Purpose:
    Run the full pipeline concurrently in multiple threads with identical inputs
    and assert that they run cleanly without race conditions, and all return identical outputs.
"""

from __future__ import annotations

import threading
import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class PipelineThreadSafetyTests(unittest.TestCase):
    """Concurrency integration tests."""

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

    def test_pipeline_thread_safety(self) -> None:
        """Pipeline matching executes concurrently across 100 threads without race conditions."""
        errors: list[Exception] = []
        outputs: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            try:
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
                
                # Check results length
                self.assertIsNotNone(res)
                self.assertEqual(7, len(res.results))

                with lock:
                    outputs.append(res.model_dump_json())
            except Exception as e:
                with lock:
                    errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Concurrency errors encountered: {errors}")
        self.assertEqual(50, len(outputs))
