"""Integration tests verifying the correctness of compiled pipeline statistics.

Purpose:
    Verify that MatchStatistics counts, category mappings, warning counts,
    and duplicate count attributes are compiled correctly.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service


class PipelineStatisticsTests(unittest.TestCase):
    """Statistics verification integration tests."""

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

    def test_pipeline_statistics_correctness(self) -> None:
        """Verify structural match statistics counts match input feature sizes."""
        # Simple resume has: 3 skills, 1 exp, 1 edu, 1 proj, 1 cert -> 7 features total
        # Simple job has: 3 skills, 1 exp, 1 edu, 1 proj, 1 cert -> 7 features total
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

        stats = res.statistics
        self.assertEqual(7, stats.total_matches)
        
        # since we combined 5 collections, total = 5 * 7 = 35, 5 * 7 = 35
        self.assertEqual(35, stats.total_resume_features)
        self.assertEqual(35, stats.total_job_features)

        self.assertEqual(0, stats.duplicate_count)
        self.assertEqual(0, stats.validation_error_count)

        # check category counts
        cat_counts = stats.category_counts
        self.assertEqual(3, cat_counts.get("SkillMatcher"))
        self.assertEqual(1, cat_counts.get("ExperienceMatcher"))
        self.assertEqual(1, cat_counts.get("EducationMatcher"))
        self.assertEqual(1, cat_counts.get("ProjectMatcher"))
        self.assertEqual(1, cat_counts.get("CertificationMatcher"))

