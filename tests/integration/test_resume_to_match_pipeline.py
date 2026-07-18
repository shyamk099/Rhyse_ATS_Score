"""Integration tests validating Happy Path entity and feature matching across all categories.

Purpose:
    Verify that Skill, Experience, Education, Certification, and Project matches
    appear correctly under simple matching scenarios.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from tests.integration.pipeline_helpers import run_full_pipeline


class ResumeToMatchPipelineTests(unittest.TestCase):
    """Happy Path integration tests checking specific category matches."""

    def setUp(self) -> None:
        """Load simple resume and job description feature collections."""
        res_path = Path("tests/fixtures/resume_simple.json")
        job_path = Path("tests/fixtures/job_simple.json")

        self.assertTrue(res_path.is_file())
        self.assertTrue(job_path.is_file())

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

    def test_happy_path_all_categories_matched(self) -> None:
        """All categories (Skill, Exp, Edu, Cert, Proj) produce at least one correct match."""
        from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
        from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules
        from tests.integration.pipeline_helpers import create_matching_service

        match_service = create_matching_service()
        
        # Test individual matchers
        rules_payload = {
            "skill_matching_rules": {"comparison_mode": "ALL"},
            "experience_matching_rules": {"comparison_mode": "ALL"},
            "education_matching_rules": {"comparison_mode": "ALL"},
            "project_matching_rules": {"comparison_mode": "ALL"},
            "certification_matching_rules": {"comparison_mode": "ALL"},
        }

        skill_col = match_service.match(self._resume_features, self._job_features, ["skill"], rules=rules_payload)
        exp_col = match_service.match(self._resume_features, self._job_features, ["experience"], rules=rules_payload)
        edu_col = match_service.match(self._resume_features, self._job_features, ["education"], rules=rules_payload)
        proj_col = match_service.match(self._resume_features, self._job_features, ["project"], rules=rules_payload)
        cert_col = match_service.match(self._resume_features, self._job_features, ["certification"], rules=rules_payload)

        # Consolidate
        canonical_match_service = CanonicalMatchCollectionService()
        res = canonical_match_service.build(
            skill_matches=skill_col,
            experience_matches=exp_col,
            education_matches=edu_col,
            project_matches=proj_col,
            certification_matches=cert_col,
            rules=CanonicalMatchingRules(),
        )

        # Verify counts and existence of each matcher type in the results
        self.assertGreaterEqual(len(res.results), 5)
        matcher_types = {r.matcher_type for r in res.results}
        self.assertIn("SkillMatcher", matcher_types)
        self.assertIn("ExperienceMatcher", matcher_types)
        self.assertIn("EducationMatcher", matcher_types)
        self.assertIn("ProjectMatcher", matcher_types)
        self.assertIn("CertificationMatcher", matcher_types)
