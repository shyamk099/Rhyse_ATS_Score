"""Integration tests checking negative matching scenarios.

Purpose:
    Verify that mismatched/different resume and job description features
    (e.g., Python vs Java, AWS vs Azure, CKA vs AWS Cert) produce zero match results.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from tests.integration.pipeline_helpers import create_matching_service, create_feature_service


class NegativeMatchingTests(unittest.TestCase):
    """Negative matching scenario tests."""

    def setUp(self) -> None:
        """Create mock mismatched feature collections."""
        def create_feature(
            feature_id: str,
            name: str,
            category: str,
            value: dict | str,
            source_id: str | None = None,
        ) -> dict:
            return {
                "feature_id": feature_id,
                "name": name,
                "category": category,
                "value": value,
                "confidence": 1.0,
                "locations": [],
                "provenance": {
                    "source_entity_id": source_id,
                    "source_entity_type": category,
                },
                "metadata": {
                    "creation_timestamp": "2026-07-13T20:00:00Z",
                    "extractor_name": "Test",
                    "version": "1.0",
                },
            }

        def create_canonical_collection(
            skills: list[dict] = None,
            experience: list[dict] = None,
            education: list[dict] = None,
            projects: list[dict] = None,
            certifications: list[dict] = None,
        ) -> dict:
            skills = skills or []
            experience = experience or []
            education = education or []
            projects = projects or []
            certifications = certifications or []
            total = len(skills) + len(experience) + len(education) + len(projects) + len(certifications)
            return {
                "skills": {"features": skills, "statistics": {"total_features_extracted": len(skills), "execution_duration_seconds": 0.0}, "context": {"correlation_id": "test", "rule_engine_config": {}, "environment": "test", "metadata": {}}},
                "experience": {"features": experience, "statistics": {"total_features_extracted": len(experience), "execution_duration_seconds": 0.0}, "context": {"correlation_id": "test", "rule_engine_config": {}, "environment": "test", "metadata": {}}},
                "education": {"features": education, "statistics": {"total_features_extracted": len(education), "execution_duration_seconds": 0.0}, "context": {"correlation_id": "test", "rule_engine_config": {}, "environment": "test", "metadata": {}}},
                "projects": {"features": projects, "statistics": {"total_features_extracted": len(projects), "execution_duration_seconds": 0.0}, "context": {"correlation_id": "test", "rule_engine_config": {}, "environment": "test", "metadata": {}}},
                "certifications": {"features": certifications, "statistics": {"total_features_extracted": len(certifications), "execution_duration_seconds": 0.0}, "context": {"correlation_id": "test", "rule_engine_config": {}, "environment": "test", "metadata": {}}},
                "statistics": {
                    "total_feature_count": total,
                    "duplicate_count": 0,
                    "validation_error_count": 0,
                    "warning_count": 0,
                },
                "validation_summary": {
                    "status": "VALID",
                    "errors": [],
                    "warnings": [],
                    "duplicate_count": 0,
                    "validation_timestamp": "2026-07-13T20:00:00Z",
                    "rules_version": "v1.0",
                },
                "metadata": {},
            }


        self._resume_features = CanonicalFeatureCollection.model_validate(
            create_canonical_collection(
                skills=[
                    create_feature("FEAT-SK-1", "Python", "SKILL", "Python", "SKL-01"),
                    create_feature("FEAT-SK-2", "AWS", "SKILL", "AWS", "SKL-02"),
                ],
                experience=[
                    create_feature("FEAT-EX-1", "Developer", "EXPERIENCE", {"company": "Google", "job_title": "Developer", "experience_id": "EXP-01"}, "EXP-01")
                ],
                education=[
                    create_feature("FEAT-ED-1", "B.Tech", "EDUCATION", {"institution": "IIT", "degree": "B.Tech", "education_id": "EDU-01"}, "EDU-01")
                ],
                projects=[
                    create_feature("FEAT-PR-1", "Project Alpha", "PROJECT", {"project_name": "Project Alpha", "project_id": "PRJ-01"}, "PRJ-01")
                ],
                certifications=[
                    create_feature("FEAT-CR-1", "AWS Certified Developer", "CERTIFICATION", {"certification_name": "AWS Certified Developer", "certification_id": "CRT-01"}, "CRT-01")
                ],
            )
        )

        self._job_features = CanonicalFeatureCollection.model_validate(
            create_canonical_collection(
                skills=[
                    create_feature("FEAT-SK-3", "Java", "SKILL", "Java", "SKL-03"),
                    create_feature("FEAT-SK-4", "Azure", "SKILL", "Azure", "SKL-04"),
                ],
                experience=[
                    create_feature("FEAT-EX-2", "Manager", "EXPERIENCE", {"company": "Meta", "job_title": "Manager", "experience_id": "EXP-02"}, "EXP-02")
                ],
                education=[
                    create_feature("FEAT-ED-2", "MBA", "EDUCATION", {"institution": "Harvard", "degree": "MBA", "education_id": "EDU-02"}, "EDU-02")
                ],
                projects=[
                    create_feature("FEAT-PR-2", "Project Beta", "PROJECT", {"project_name": "Project Beta", "project_id": "PRJ-02"}, "PRJ-02")
                ],
                certifications=[
                    create_feature("FEAT-CR-2", "CKA", "CERTIFICATION", {"certification_name": "CKA", "certification_id": "CRT-02"}, "CRT-02")
                ],
            )
        )

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_mismatched_features_produce_zero_matches(self) -> None:
        """mismatched features do not produce any matches in all categories."""
        rules_payload = {
            "skill_matching_rules": {"comparison_mode": "ALL"},
            "experience_matching_rules": {"comparison_mode": "ALL"},
            "education_matching_rules": {"comparison_mode": "ALL"},
            "project_matching_rules": {"comparison_mode": "ALL"},
            "certification_matching_rules": {"comparison_mode": "ALL"},
        }

        skill_col = self._match_service.match(self._resume_features, self._job_features, ["skill"], rules=rules_payload)
        exp_col = self._match_service.match(self._resume_features, self._job_features, ["experience"], rules=rules_payload)
        edu_col = self._match_service.match(self._resume_features, self._job_features, ["education"], rules=rules_payload)
        proj_col = self._match_service.match(self._resume_features, self._job_features, ["project"], rules=rules_payload)
        cert_col = self._match_service.match(self._resume_features, self._job_features, ["certification"], rules=rules_payload)

        res = self._canonical_match_service.build(
            skill_matches=skill_col,
            experience_matches=exp_col,
            education_matches=edu_col,
            project_matches=proj_col,
            certification_matches=cert_col,
        )

        # Output collection contains 0 results because nothing matched
        self.assertEqual(0, len(res.results))
        self.assertEqual(0, res.statistics.total_matches)
