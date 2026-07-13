"""Unit and Integration tests for Education Feature Engineering.

Purpose:
    Verify Education entity mapping, structural whitespace normalization, required validation rules,
    1:1 education entity preservation (Refinement 3), None-preservation for raw/missing details (Refinement 2),
    warning generation, registry lookup, and parallel thread safety.
"""

from __future__ import annotations

import threading
import unittest
from typing import Mapping

from ats_engine.domain.entity_extraction.canonical.canonical_models import (
    CanonicalEntityCollection,
    EntityStatistics,
    ValidationSummary,
)
from ats_engine.domain.entity_extraction.certification.certification_models import (
    CertificationCollection,
    CertificationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.education.education_models import (
    EducationCollection,
    EducationEntity,
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
from ats_engine.domain.feature_engineering.education.extractor import EducationFeatureExtractor
from ats_engine.domain.feature_engineering.education.normalizer import EducationFeatureNormalizer
from ats_engine.domain.feature_engineering.education.validator import EducationFeatureValidator


class EducationFeatureEngineeringTests(unittest.TestCase):
    """Test suite validating EducationFeatureExtractor lifecycle and refinements."""

    def setUp(self) -> None:
        """Initialize service wrapper and mock entity objects."""
        self._service = FeatureEngineeringService()
        self._extractor = EducationFeatureExtractor()

    def _create_mock_canonical(
        self,
        edu_entities: list[EducationEntity],
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
                entities=tuple(edu_entities),
                statistics=EducationExtractionStatistics(
                    total_education_records=len(edu_entities),
                    records_with_degree=sum(1 for e in edu_entities if e.degree),
                    records_with_gpa=sum(1 for e in edu_entities if e.gpa_raw),
                    execution_duration_seconds=0.01,
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
                entities=(),
                statistics=CertificationExtractionStatistics(
                    total_certifications=0,
                    active_certifications=0,
                    execution_duration_seconds=0.0,
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
                education_count=len(edu_entities),
                project_count=0,
                certification_count=0,
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.01,
            ),
        )

    def test_extracts_canonical_education_to_feature(self) -> None:
        """Extractor maps valid canonical education to a generic Feature DTO."""
        entity = EducationEntity(
            education_id="EDU-01",
            institution_name="Stanford University",
            degree="Bachelor of Science",
            specialization="AI",
            field_of_study="Computer Science",
            start_date_raw="2020-09",
            end_date_raw="2024-06",
            graduation_date_raw="2024-06",
            gpa_raw="3.9",
            grade_raw="A",
            honors=("Magna Cum Laude",),
            certifications=("AWS Certified",),
            location_raw="Stanford, CA",
            confidence=0.98,
            confidence_reason="Verified degree matches",
            matched_rules=("edu_rule1",),
            source_segment_ids=("seg_1",),
            source_text="Studied CS at Stanford...",
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_edu")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-EDUCATION-EDU-01", feat.feature_id)
        self.assertEqual("Bachelor of Science", feat.name)
        self.assertEqual(FeatureCategory.EDUCATION, feat.category)  # Refinement 5
        self.assertEqual(0.98, feat.confidence)
        self.assertEqual("EDU-01", feat.provenance.source_entity_id)  # Refinement 4
        self.assertEqual("EDUCATION", feat.provenance.source_entity_type)

        # Refinement 11: structured value mapping (using uniform naming specification)
        val = feat.value
        self.assertEqual("Stanford University", val["institution"])
        self.assertEqual("Bachelor of Science", val["degree"])
        self.assertEqual("Computer Science", val["major"])
        self.assertEqual("AI", val["specialization"])
        self.assertEqual("2020-09", val["start_date_raw"])
        self.assertEqual("2024-06", val["end_date_raw"])
        self.assertEqual("2024-06", val["graduation_date_raw"])
        self.assertEqual("3.9", val["gpa"])
        self.assertEqual("A", val["grade"])
        self.assertEqual(("Magna Cum Laude",), val["honors"])
        self.assertEqual(("AWS Certified",), val["certifications"])
        self.assertEqual("Stanford, CA", val["location"])
        self.assertNotIn("study_years", val)  # Refinement 1 (no study duration)

    def test_retains_exactly_one_feature_per_record(self) -> None:
        """Extractor preserves 1:1 mapping and does not split education (Refinement 3)."""
        entity1 = EducationEntity(
            education_id="EDU-01",
            institution_name="MIT",
            degree="MS",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        entity2 = EducationEntity(
            education_id="EDU-02",
            institution_name="Stanford",
            degree="PhD",
            confidence=0.8,
            source_segment_ids=("seg_2",),
        )
        canonical = self._create_mock_canonical([entity1, entity2])
        context = FeatureExtractionContext(correlation_id="test_corr_one_feature")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(2, len(features))
        self.assertEqual("FEAT-EDUCATION-EDU-01", features[0].feature_id)
        self.assertEqual("FEAT-EDUCATION-EDU-02", features[1].feature_id)

    def test_whitespace_normalization_only(self) -> None:
        """Normalizer trims whitespace and duplicate spaces without changing canonical texts (Refinement 6)."""
        entity = EducationEntity(
            education_id="EDU-01",
            institution_name="  Stanford   University  ",
            degree="Master    of Science",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_norm")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        val = features[0].value
        self.assertEqual("Stanford University", val["institution"])
        self.assertEqual("Master of Science", val["degree"])

    def test_validation_exception_handling(self) -> None:
        """Validator raises ValueError when required fields are missing or threshold is not met."""
        entity = EducationEntity(
            education_id="EDU-01",
            institution_name="Stanford",
            confidence=0.4,  # Below threshold
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        rules = {
            "education_feature_rules": {
                "confidence_threshold": 0.5,
            }
        }
        context = FeatureExtractionContext(
            correlation_id="test_corr_val_fail",
            rule_engine_config=rules,
        )

        with self.assertRaises(ValueError):
            self._extractor.extract(canonical, context)

    def test_empty_education_collection_handling(self) -> None:
        """Extractor handles empty collections and returns empty arrays gracefully."""
        canonical = self._create_mock_canonical([])
        context = FeatureExtractionContext(correlation_id="test_corr_empty")
        features = self._extractor.extract(canonical, context)
        self.assertEqual(0, len(features))

    def test_registry_and_pipeline_integration(self) -> None:
        """E2E pipeline integrates and runs dynamically registered EducationFeatureExtractor successfully."""
        self._service.registry.register("education_features", EducationFeatureExtractor)

        entity = EducationEntity(
            education_id="EDU-02",
            institution_name="MIT",
            degree="Bachelor of Science",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])

        collection = self._service.extract_features(
            canonical,
            enabled_extractors=["education_features"],
        )

        self.assertEqual(1, len(collection.features))
        self.assertEqual("FEAT-EDUCATION-EDU-02", collection.features[0].feature_id)
        self.assertIn("EducationFeatureExtractor", collection.statistics.extractor_counts)

    def test_thread_safety_under_concurrent_extractions(self) -> None:
        """Extractor executes concurrently without shared mutable state failures."""
        entity = EducationEntity(
            education_id="EDU-01",
            institution_name="Harvard",
            degree="MBA",
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
