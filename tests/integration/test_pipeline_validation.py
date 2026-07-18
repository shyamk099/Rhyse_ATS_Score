"""Integration tests verifying pipeline validation constraints and summary generation.

Purpose:
    Verify that ValidationSummary, ValidationErrorDetail, and ValidationWarningDetail DTOs
    are populated correctly under strict and lenient validation configurations.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules
from ats_engine.domain.matching.exceptions import MatchValidationError
from tests.integration.pipeline_helpers import create_matching_service


class PipelineValidationTests(unittest.TestCase):
    """Validation engine integration tests."""

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

    def test_lenient_validation_captures_errors_without_crashing(self) -> None:
        """In LENIENT mode, structural errors are recorded but no exception is raised."""
        # Intentionally inject bad match result (missing provenance)
        skill_col = self._match_service.match(self._resume_features, self._job_features, ["skill"])
        
        # Corrupt one result's provenance
        corrupted_results = list(skill_col.results)
        if corrupted_results:
            r = corrupted_results[0]
            corrupted_results[0] = r.model_copy(update={"provenance": None})
            
        corrupted_skill_col = skill_col.model_copy(update={"results": tuple(corrupted_results)})
        empty = corrupted_skill_col.model_copy(update={"results": ()})

        rules_lenient = CanonicalMatchingRules(validation_mode="LENIENT")
        res = self._canonical_match_service.build(
            skill_matches=corrupted_skill_col,
            experience_matches=empty,
            education_matches=empty,
            project_matches=empty,
            certification_matches=empty,
            rules=rules_lenient,
        )

        summary = res.validation_summary
        self.assertEqual(1, summary.total_errors)
        self.assertEqual("provenance", summary.errors[0].field)
        self.assertEqual("error", summary.errors[0].severity)

    def test_strict_validation_raises_exception(self) -> None:
        """In STRICT mode, structural errors trigger a MatchValidationError."""
        skill_col = self._match_service.match(self._resume_features, self._job_features, ["skill"])
        corrupted_results = list(skill_col.results)
        if corrupted_results:
            r = corrupted_results[0]
            corrupted_results[0] = r.model_copy(update={"provenance": None})
            
        corrupted_skill_col = skill_col.model_copy(update={"results": tuple(corrupted_results)})
        empty = corrupted_skill_col.model_copy(update={"results": ()})

        rules_strict = CanonicalMatchingRules(validation_mode="STRICT")
        with self.assertRaises(MatchValidationError):
            self._canonical_match_service.build(
                skill_matches=corrupted_skill_col,
                experience_matches=empty,
                education_matches=empty,
                project_matches=empty,
                certification_matches=empty,
                rules=rules_strict,
            )
