"""Unit and Integration tests for Feature Engineering Foundation.

Purpose:
    Verify registry mappings, exception propagation, sequential pipeline flow,
    service wrappers, context delivery, immutable models, and multi-thread safety.
"""

from __future__ import annotations

import threading
import time
import unittest
from typing import Sequence

from pydantic import ValidationError

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
from ats_engine.domain.feature_engineering.exceptions import (
    PipelineExecutionError,
    RegistrationError,
    UnknownExtractorError,
)
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.factory import FeatureExtractorFactory
from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    FeatureExtractionContext,
    FeatureLocation,
    FeatureMetadata,
    FeatureProvenance,
)
from ats_engine.domain.feature_engineering.pipeline import FeatureEngineeringPipeline
from ats_engine.domain.feature_engineering.registry import FeatureExtractorRegistry
from ats_engine.domain.feature_engineering.service import FeatureEngineeringService


class MockExtractorA(FeatureExtractor):
    """Mock extractor producing a static mock feature sequence."""

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        meta = FeatureMetadata(
            creation_timestamp="2026-07-13T20:00:00Z",
            extractor_name="MockExtractorA",
            version="1.0",
        )
        prov = FeatureProvenance(
            source_entity_id="ENT-A",
            source_entity_type="mock_type",
            source_section="SUMMARY",
        )
        feat = Feature(
            feature_id="FEAT-A-01",
            name="Mock Feature A",
            category=FeatureCategory.SKILL,
            value="Mock Value A",
            confidence=0.9,
            locations=(FeatureLocation(page_number=1),),
            provenance=prov,
            metadata=meta,
        )
        return [feat]


class MockExtractorB(FeatureExtractor):
    """Mock extractor producing another static feature sequence."""

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        meta = FeatureMetadata(
            creation_timestamp="2026-07-13T20:00:00Z",
            extractor_name="MockExtractorB",
            version="1.1",
        )
        prov = FeatureProvenance(
            source_entity_id="ENT-B",
            source_entity_type="mock_type_b",
        )
        feat = Feature(
            feature_id="FEAT-B-01",
            name="Mock Feature B",
            category=FeatureCategory.EXPERIENCE,
            value=42.0,
            confidence=1.0,
            provenance=prov,
            metadata=meta,
        )
        return [feat]


class FailingMockExtractor(FeatureExtractor):
    """Mock extractor designed to fail for error test flows."""

    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        raise ValueError("Simulated extractor processing error.")


class FeatureEngineeringFoundationTests(unittest.TestCase):
    """Verify registry, factory, pipeline, models and service layers."""

    def setUp(self) -> None:
        """Initialize pipeline elements and empty collection mocks."""
        self._registry = FeatureExtractorRegistry()
        self._factory = FeatureExtractorFactory(self._registry)
        self._pipeline = FeatureEngineeringPipeline()
        self._service = FeatureEngineeringService()

        # Build blank CanonicalEntityCollection DTO
        self._empty_canonical = CanonicalEntityCollection(
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
                education_count=0,
                project_count=0,
                certification_count=0,
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.0,
            ),
        )

    def test_registry_registration_and_lookup(self) -> None:
        """Registry stores classes, rejects duplicates, and maps case-insensitively."""
        self._registry.register("MOCK_A", MockExtractorA)
        self.assertTrue(self._registry.is_registered("mock_a"))
        self.assertTrue(self._registry.is_registered("MoCk_A"))

        # Rejects duplicates
        with self.assertRaises(RegistrationError):
            self._registry.register("mock_a", MockExtractorA)

        # Rejects empty keys
        with self.assertRaises(RegistrationError):
            self._registry.register(" ", MockExtractorA)

    def test_factory_instantiates_stateless_classes(self) -> None:
        """Factory creates unique instances from registered class keys, raising errors for unknown types."""
        self._registry.register("mock_a", MockExtractorA)
        
        inst1 = self._factory.get_extractor("mock_a")
        inst2 = self._factory.get_extractor("mock_a")

        self.assertIsInstance(inst1, MockExtractorA)
        self.assertIsInstance(inst2, MockExtractorA)
        self.assertIsNot(inst1, inst2)  # Dynamically instantiated

        with self.assertRaises(UnknownExtractorError):
            self._factory.get_extractor("unknown_key")

    def test_pipeline_sequential_execution_and_statistics(self) -> None:
        """Pipeline executes extractors in sequence, aggregates features, and compiles duration stats."""
        extractors = [MockExtractorA(), MockExtractorB()]
        context = FeatureExtractionContext(correlation_id="test_corr_123")

        collection = self._pipeline.execute(self._empty_canonical, extractors, context)

        self.assertEqual(2, len(collection.features))
        self.assertEqual("FEAT-A-01", collection.features[0].feature_id)
        self.assertEqual("FEAT-B-01", collection.features[1].feature_id)
        self.assertEqual(2, collection.statistics.total_features_extracted)
        self.assertIn("MockExtractorA", collection.statistics.extractor_counts)
        self.assertIn("MockExtractorB", collection.statistics.extractor_counts)
        self.assertGreater(collection.statistics.execution_duration_seconds, 0.0)

    def test_pipeline_wraps_extractor_exceptions(self) -> None:
        """Pipeline catches extractor exceptions and wraps them in a PipelineExecutionError."""
        extractors = [FailingMockExtractor()]
        context = FeatureExtractionContext(correlation_id="test_corr_fail")

        with self.assertRaises(PipelineExecutionError):
            self._pipeline.execute(self._empty_canonical, extractors, context)

    def test_service_orchestration(self) -> None:
        """Service coordinates loading, instantiation, and pipeline flow returning FeatureCollection."""
        self._service.registry.register("mock_a", MockExtractorA)
        self._service.registry.register("mock_b", MockExtractorB)

        collection = self._service.extract_features(
            self._empty_canonical,
            enabled_extractors=["mock_a", "mock_b"],
        )

        self.assertEqual(2, len(collection.features))
        self.assertEqual("FEAT-A-01", collection.features[0].feature_id)
        self.assertEqual("FEAT-B-01", collection.features[1].feature_id)
        self.assertEqual("VALID", collection.context.rule_engine_config.get("status", "VALID"))

    def test_models_immutability(self) -> None:
        """Models are frozen and raise Pydantic errors upon mutation attempts."""
        loc = FeatureLocation(page_number=1)
        with self.assertRaises(ValidationError):
            loc.page_number = 2  # type: ignore

    def test_thread_safety_under_concurrent_registrations(self) -> None:
        """Registry handles concurrent registrations and reads across threads cleanly."""
        errors: list[Exception] = []

        def register_task(index: int) -> None:
            try:
                self._registry.register(f"thread_extractor_{index}", MockExtractorA)
                self._registry.get(f"thread_extractor_{index}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=register_task, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread execution raised errors: {errors}")
        self.assertEqual(50, len(self._registry._registry))

    def test_empty_feature_collection(self) -> None:
        """Pipeline returns empty FeatureCollection when no extractors are enabled."""
        context = FeatureExtractionContext(correlation_id="test_corr_empty")
        collection = self._pipeline.execute(self._empty_canonical, [], context)
        self.assertEqual(0, len(collection.features))
        self.assertEqual(0, collection.statistics.total_features_extracted)
