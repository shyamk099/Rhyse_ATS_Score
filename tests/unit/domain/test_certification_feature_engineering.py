"""Unit and Integration tests for Certification Feature Engineering.

Purpose:
    Verify Certification entity mapping, whitespace normalization, validation rules,
    1:1 certification entity preservation, None-preservation for raw/missing details,
    warning generation, registry lookup, and parallel thread safety.
"""

from __future__ import annotations

import threading
import unittest

from ats_engine.domain.entity_extraction.canonical.canonical_models import (
    CanonicalEntityCollection,
    EntityStatistics,
    ValidationSummary,
)
from ats_engine.domain.entity_extraction.certification.certification_models import (
    CertificationCollection,
    CertificationEntity,
    CertificationExtractionStatistics,
    CertificationURL,
)
from ats_engine.domain.entity_extraction.education.education_models import (
    EducationCollection,
    EducationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.experience.experience_models import (
    ExperienceCollection,
    ExperienceExtractionStatistics,
)
from ats_engine.domain.entity_extraction.models import (
    EntityCollection,
    EntityExtractionStatistics,
)
from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectCollection,
    ProjectExtractionStatistics,
)
from ats_engine.domain.entity_extraction.skills.skill_models import (
    SkillCollection,
    SkillExtractionStatistics,
)
from ats_engine.domain.feature_engineering.models import FeatureCategory, FeatureExtractionContext
from ats_engine.domain.feature_engineering.service import FeatureEngineeringService
from ats_engine.domain.feature_engineering.certification.extractor import CertificationFeatureExtractor


class CertificationFeatureEngineeringTests(unittest.TestCase):
    """Test suite validating CertificationFeatureExtractor lifecycle and refinements."""

    def setUp(self) -> None:
        """Initialize service wrapper and mock entity objects."""
        self._service = FeatureEngineeringService()
        self._extractor = CertificationFeatureExtractor()

    def _create_mock_canonical(
        self,
        cert_entities: list[CertificationEntity],
    ) -> CanonicalEntityCollection:
        """Helper to create dummy canonical entity collections."""
        return CanonicalEntityCollection(
            contacts=EntityCollection(
                entities=(),
                statistics=EntityExtractionStatistics(
                    total_entities=0, execution_duration_seconds=0.0
                ),
            ),
            skills=SkillCollection(
                entities=(),
                statistics=SkillExtractionStatistics(
                    total_skills_found=0,
                    unique_skills_count=0,
                    execution_duration_seconds=0.0,
                ),
            ),
            experiences=ExperienceCollection(
                entities=(),
                statistics=ExperienceExtractionStatistics(
                    total_experiences=0,
                    current_employment_count=0,
                    execution_duration_seconds=0.0,
                ),
            ),
            education=EducationCollection(
                entities=(),
                statistics=EducationExtractionStatistics(
                    total_education_records=0,
                    records_with_degree=0,
                    records_with_gpa=0,
                    execution_duration_seconds=0.0,
                ),
            ),
            projects=ProjectCollection(
                entities=(),
                statistics=ProjectExtractionStatistics(
                    total_projects=0,
                    projects_with_repo=0,
                    projects_with_demo=0,
                    execution_duration_seconds=0.0,
                ),
            ),
            certifications=CertificationCollection(
                entities=tuple(cert_entities),
                statistics=CertificationExtractionStatistics(
                    total_certifications=len(cert_entities),
                    active_certifications=sum(
                        1 for e in cert_entities if e.validity_status_raw == "active"
                    ),
                    execution_duration_seconds=0.01,
                ),
            ),
            validation_summary=ValidationSummary(
                status="VALID",
                validation_timestamp="2026-07-13T20:00:00Z",
                rules_version="rules_v1.0",
            ),
            statistics=EntityStatistics(
                contact_count=0,
                skill_count=0,
                experience_count=0,
                education_count=0,
                project_count=0,
                certification_count=len(cert_entities),
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.01,
            ),
        )

    def test_extracts_canonical_certification_to_feature(self) -> None:
        """Extractor maps valid canonical certification to a generic Feature DTO."""
        entity = CertificationEntity(
            certification_id="CERT-01",
            certification_name="Google Cloud Professional Cloud Architect",
            issuing_organization="Google Cloud",
            credential_id_raw="GCP-PCA-12345",
            credential_url=CertificationURL(
                original_value="http://gcp.url",
                normalized_value="https://gcp.url",
                matched_rule="url_rule",
            ),
            issue_date_raw="2024-01",
            expiration_date_raw="2026-01",
            validity_status_raw="active",
            associated_skill_ids=("SKL-GCP", "SKL-ARC"),
            associated_skills_raw=("Google Cloud Platform", "Cloud Architecture"),
            description_raw="Professional Cloud Architect GCP Certificate",
            confidence=0.97,
            confidence_reason="Verified credential info",
            matched_rules=("cert_rule1",),
            source_segment_ids=("seg_1",),
            source_text="Holds Google Cloud Professional Architect GCP Cloud Architecture...",
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_cert")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-CERTIFICATION-CERT-01", feat.feature_id)
        self.assertEqual("Google Cloud Professional Cloud Architect", feat.name)
        self.assertEqual(FeatureCategory.CERTIFICATION, feat.category)
        self.assertEqual(0.97, feat.confidence)
        self.assertEqual("CERT-01", feat.provenance.source_entity_id)

        # check generic values
        val = feat.value
        self.assertEqual("Google Cloud Professional Cloud Architect", val["certification_name"])
        self.assertEqual("Google Cloud", val["issuing_organization"])
        self.assertEqual("GCP-PCA-12345", val["credential_id"])
        self.assertEqual("https://gcp.url", val["credential_url"]["normalized_value"])
        self.assertEqual("2024-01", val["issue_date_raw"])
        self.assertEqual("2026-01", val["expiration_date_raw"])
        self.assertEqual("active", val["validity_status_raw"])
        self.assertEqual(("SKL-GCP", "SKL-ARC"), val["associated_skill_ids"])
        self.assertEqual(("Google Cloud Platform", "Cloud Architecture"), val["associated_skills"])
        self.assertEqual("Professional Cloud Architect GCP Certificate", val["description"])

    def test_retains_exactly_one_feature_per_record(self) -> None:
        """Extractor preserves 1:1 mapping and does not split certification records (Refinement 3)."""
        entity1 = CertificationEntity(
            certification_id="CERT-01",
            certification_name="Cert One",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        entity2 = CertificationEntity(
            certification_id="CERT-02",
            certification_name="Cert Two",
            confidence=0.8,
            source_segment_ids=("seg_2",),
        )
        canonical = self._create_mock_canonical([entity1, entity2])
        context = FeatureExtractionContext(correlation_id="test_corr_one_feature")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(2, len(features))
        self.assertEqual("FEAT-CERTIFICATION-CERT-01", features[0].feature_id)
        self.assertEqual("FEAT-CERTIFICATION-CERT-02", features[1].feature_id)

    def test_whitespace_normalization_only(self) -> None:
        """Normalizer trims whitespace and duplicate spaces without changing canonical texts (Refinement 6)."""
        entity = CertificationEntity(
            certification_id="CERT-01",
            certification_name="  Professional   Cloud   Architect  ",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_norm")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        val = features[0].value
        self.assertEqual("Professional Cloud Architect", val["certification_name"])

    def test_validation_exception_handling(self) -> None:
        """Validator raises ValueError when required fields are missing or threshold is not met."""
        entity = CertificationEntity(
            certification_id="CERT-01",
            certification_name="Cert Fail",
            confidence=0.2,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        rules = {
            "certification_feature_rules": {
                "confidence_threshold": 0.5,
            }
        }
        context = FeatureExtractionContext(
            correlation_id="test_corr_val_fail",
            rule_engine_config=rules,
        )

        with self.assertRaises(ValueError):
            self._extractor.extract(canonical, context)

    def test_registry_and_pipeline_integration(self) -> None:
        """E2E pipeline integrates and runs dynamically registered CertificationFeatureExtractor successfully."""
        self._service.registry.register("certification_features", CertificationFeatureExtractor)

        entity = CertificationEntity(
            certification_id="CERT-02",
            certification_name="Registered Certification",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])

        collection = self._service.extract_features(
            canonical,
            enabled_extractors=["certification_features"],
        )

        self.assertEqual(1, len(collection.features))
        self.assertEqual("FEAT-CERTIFICATION-CERT-02", collection.features[0].feature_id)

    def test_thread_safety_under_concurrent_extractions(self) -> None:
        """Extractor executes concurrently without shared mutable state failures."""
        entity = CertificationEntity(
            certification_id="CERT-01",
            certification_name="Parallel Certification",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_thread_corr")

        errors: list[Exception] = []

        def run_extraction() -> None:
            try:
                features = self._extractor.extract(canonical, context)
                self.assertEqual(1, len(features))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run_extraction) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Concurrent executions raised exceptions: {errors}")
