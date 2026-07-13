"""Unit and Integration tests for Experience Feature Engineering.

Purpose:
    Verify Experience entity mapping, structural whitespace normalization, required validation rules,
    1:1 job entity preservation (Refinement 3), None-preservation for raw/missing details (Refinement 2),
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
    EducationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.experience.experience_models import (
    ExperienceCollection,
    ExperienceEntity,
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
from ats_engine.domain.feature_engineering.experience.extractor import ExperienceFeatureExtractor
from ats_engine.domain.feature_engineering.experience.normalizer import ExperienceFeatureNormalizer
from ats_engine.domain.feature_engineering.experience.validator import ExperienceFeatureValidator


class ExperienceFeatureEngineeringTests(unittest.TestCase):
    """Test suite validating ExperienceFeatureExtractor lifecycle and refinements."""

    def setUp(self) -> None:
        """Initialize service wrapper and mock entity objects."""
        self._service = FeatureEngineeringService()
        self._extractor = ExperienceFeatureExtractor()

    def _create_mock_canonical(
        self,
        exp_entities: list[ExperienceEntity],
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
                entities=tuple(exp_entities),
                statistics=ExperienceExtractionStatistics(
                    total_experiences=len(exp_entities),
                    current_employment_count=sum(1 for e in exp_entities if e.is_current),
                    execution_duration_seconds=0.01,
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
                experience_count=len(exp_entities),
                education_count=0,
                project_count=0,
                certification_count=0,
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.01,
            ),
        )

    def test_extracts_canonical_experience_to_feature(self) -> None:
        """Extractor maps valid canonical experience to a generic Feature DTO."""
        entity = ExperienceEntity(
            experience_id="EXP-01",
            company_name="Google",
            job_title="Software Engineer",
            employment_type="Full-time",
            start_date_raw="2024-01",
            end_date_raw=None,
            is_current=True,
            responsibilities=("Writing code", "Pair programming"),
            technologies=("Python", "C++"),
            achievements=(),
            confidence=0.95,
            confidence_reason="Strong matches found",
            matched_rules=("rule1",),
            source_segment_ids=("seg_1", "seg_2"),
            source_text="Worked at Google...",
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_exp")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-EXPERIENCE-EXP-01", feat.feature_id)
        self.assertEqual("Software Engineer", feat.name)
        self.assertEqual(FeatureCategory.EXPERIENCE, feat.category)  # Refinement 1
        self.assertEqual(0.95, feat.confidence)
        self.assertEqual("EXP-01", feat.provenance.source_entity_id)  # Refinement 4
        self.assertEqual("EXPERIENCE", feat.provenance.source_entity_type)

        # Refinement 2: structured value mapping
        val = feat.value
        self.assertEqual("Google", val["company"])
        self.assertEqual("Software Engineer", val["job_title"])
        self.assertEqual("Full-time", val["employment_type"])
        self.assertEqual("2024-01", val["start_date_raw"])
        self.assertIsNone(val["end_date_raw"])  # Refinement 2 (no inference)
        self.assertTrue(val["is_current"])
        self.assertNotIn("duration_months", val)  # Refinement 1 (no duration math)

    def test_retains_exactly_one_feature_per_job(self) -> None:
        """Extractor preserves 1:1 mapping and does not split jobs (Refinement 3)."""
        entity1 = ExperienceEntity(
            experience_id="EXP-01",
            company_name="Google",
            job_title="SWE",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        entity2 = ExperienceEntity(
            experience_id="EXP-02",
            company_name="Meta",
            job_title="Production Engineer",
            confidence=0.8,
            source_segment_ids=("seg_2",),
        )
        canonical = self._create_mock_canonical([entity1, entity2])
        context = FeatureExtractionContext(correlation_id="test_corr_one_feature")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(2, len(features))
        self.assertEqual("FEAT-EXPERIENCE-EXP-01", features[0].feature_id)
        self.assertEqual("FEAT-EXPERIENCE-EXP-02", features[1].feature_id)

    def test_whitespace_normalization_only(self) -> None:
        """Normalizer trims whitespace and duplicate spaces without changing canonical texts (Refinement 6)."""
        entity = ExperienceEntity(
            experience_id="EXP-01",
            company_name="  Google   LLC  ",
            job_title="Senior    Software Engineer",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_norm")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        val = features[0].value
        self.assertEqual("Google LLC", val["company"])
        self.assertEqual("Senior Software Engineer", val["job_title"])

    def test_validation_exception_handling(self) -> None:
        """Validator raises ValueError when required fields are missing or threshold is not met."""
        entity = ExperienceEntity(
            experience_id="EXP-01",
            company_name="Google",
            confidence=0.4,  # Below threshold
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        rules = {
            "experience_feature_rules": {
                "confidence_threshold": 0.5,
            }
        }
        context = FeatureExtractionContext(
            correlation_id="test_corr_val_fail",
            rule_engine_config=rules,
        )

        with self.assertRaises(ValueError):
            self._extractor.extract(canonical, context)

    def test_empty_experience_collection_handling(self) -> None:
        """Extractor handles empty collections and returns empty arrays gracefully."""
        canonical = self._create_mock_canonical([])
        context = FeatureExtractionContext(correlation_id="test_corr_empty")
        features = self._extractor.extract(canonical, context)
        self.assertEqual(0, len(features))

    def test_registry_and_pipeline_integration(self) -> None:
        """E2E pipeline integrates and runs dynamically registered ExperienceFeatureExtractor successfully."""
        self._service.registry.register("experience_features", ExperienceFeatureExtractor)

        entity = ExperienceEntity(
            experience_id="EXP-02",
            company_name="Apple",
            job_title="Hardware Engineer",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])

        collection = self._service.extract_features(
            canonical,
            enabled_extractors=["experience_features"],
        )

        self.assertEqual(1, len(collection.features))
        self.assertEqual("FEAT-EXPERIENCE-EXP-02", collection.features[0].feature_id)
        self.assertIn("ExperienceFeatureExtractor", collection.statistics.extractor_counts)

    def test_thread_safety_under_concurrent_extractions(self) -> None:
        """Extractor executes concurrently without shared mutable state failures."""
        entity = ExperienceEntity(
            experience_id="EXP-01",
            company_name="Netflix",
            job_title="Manager",
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
