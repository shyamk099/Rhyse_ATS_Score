"""Unit and Integration tests for Skill Feature Engineering.

Purpose:
    Verify Skill entity mapping, structural whitespace normalization, required validation rules,
    duplicate skill grouping (Refinement 4), None-preservation for raw skill IDs (Refinement 1),
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
    ExperienceExtractionStatistics,
)
from ats_engine.domain.entity_extraction.models import (
    EntityCollection,
    EntityExtractionStatistics,
    EntityLocation,
    ExtractedEntity,
)
from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectCollection,
    ProjectExtractionStatistics,
)
from ats_engine.domain.entity_extraction.skills.skill_models import (
    SkillCollection,
    SkillExtractionStatistics,
)
from ats_engine.domain.feature_engineering.models import FeatureExtractionContext
from ats_engine.domain.feature_engineering.service import FeatureEngineeringService
from ats_engine.domain.feature_engineering.skills.extractor import SkillFeatureExtractor
from ats_engine.domain.feature_engineering.skills.normalizer import SkillFeatureNormalizer
from ats_engine.domain.feature_engineering.skills.validator import SkillFeatureValidator


class SkillFeatureEngineeringTests(unittest.TestCase):
    """Test suite validating SkillFeatureExtractor lifecycle and refinements."""

    def setUp(self) -> None:
        """Initialize service wrapper and mock entity objects."""
        self._service = FeatureEngineeringService()
        self._extractor = SkillFeatureExtractor()

    def _create_mock_canonical(
        self,
        skills_entities: list[ExtractedEntity],
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
                entities=tuple(skills_entities),
                statistics=SkillExtractionStatistics(
                    total_skills_found=len(skills_entities),
                    unique_skills_count=len(set(e.value for e in skills_entities)),
                    execution_duration_seconds=0.01,
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
                skill_count=len(skills_entities),
                experience_count=0,
                education_count=0,
                project_count=0,
                certification_count=0,
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.01,
            ),
        )

    def test_extracts_canonical_skill_to_feature(self) -> None:
        """Extractor maps valid canonical skill to a generic Feature DTO."""
        entity = ExtractedEntity(
            entity_type="SKILL",
            value="Python",
            confidence=0.95,
            location=EntityLocation(segment_id="seg_1", start_char=10, end_char=16),
            metadata={
                "skill_id": "SKL-01",
                "category": "programming_language",
                "document_name": "resume.pdf",
            },
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_skill")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-SKILL-SKL-01", feat.feature_id)
        self.assertEqual("Python", feat.name)
        self.assertEqual("SKILL", feat.category)
        self.assertEqual("Python", feat.value)
        self.assertEqual(0.95, feat.confidence)
        self.assertEqual("SKL-01", feat.provenance.source_entity_id)
        self.assertEqual("SKILL", feat.provenance.source_entity_type)
        self.assertEqual("resume.pdf", feat.provenance.source_document)

        # Telemetry verification
        self.assertEqual(1, feat.metadata.custom_attributes.get("occurrence_count"))
        self.assertEqual("programming_language", feat.metadata.custom_attributes.get("category"))
        self.assertTrue(feat.metadata.custom_attributes.get("is_canonical"))

    def test_aggregates_duplicate_occurrences(self) -> None:
        """Extractor aggregates duplicate occurrences of the same skill into ONE feature with count (Refinement 4)."""
        entity1 = ExtractedEntity(
            entity_type="SKILL",
            value="Python",
            confidence=0.9,
            location=EntityLocation(segment_id="seg_1", start_char=10, end_char=16),
            metadata={"skill_id": "SKL-01", "section_type": "SKILLS"},
        )
        entity2 = ExtractedEntity(
            entity_type="SKILL",
            value="Python",
            confidence=1.0,
            location=EntityLocation(segment_id="seg_2", start_char=50, end_char=56),
            metadata={"skill_id": "SKL-01", "section_type": "EXPERIENCE"},
        )
        canonical = self._create_mock_canonical([entity1, entity2])
        context = FeatureExtractionContext(correlation_id="test_corr_dup")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-SKILL-SKL-01", feat.feature_id)
        self.assertEqual(2, feat.metadata.custom_attributes.get("occurrence_count"))
        self.assertEqual(0.95, feat.confidence)  # Average confidence
        self.assertEqual(2, len(feat.locations))
        self.assertIn("SKILLS", feat.provenance.source_section)
        self.assertIn("EXPERIENCE", feat.provenance.source_section)

    def test_missing_canonical_id_preserves_none(self) -> None:
        """Extractor preserves None for unregistered skill IDs, mapping names raw (Refinement 1)."""
        entity = ExtractedEntity(
            entity_type="SKILL",
            value="Git Flow",
            confidence=0.8,
            location=EntityLocation(segment_id="seg_1", start_char=0, end_char=8),
            metadata={"category": "tools"},  # Missing skill_id
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_none")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-SKILL-RAW-git_flow", feat.feature_id)
        self.assertEqual("Git Flow", feat.name)
        self.assertIsNone(feat.provenance.source_entity_id)  # Preserves None!
        self.assertFalse(feat.metadata.custom_attributes.get("is_canonical"))

    def test_structural_normalization_only(self) -> None:
        """Normalizer trims whitespace and duplicate spaces, but does not alter canonical definitions (Refinement 3)."""
        entity = ExtractedEntity(
            entity_type="SKILL",
            value="  AWS   Cloud  ",  # Duplicate spacing
            confidence=0.8,
            location=EntityLocation(segment_id="seg_1", start_char=0, end_char=10),
            metadata={"skill_id": "SKL-03"},
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_norm")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        self.assertEqual("AWS Cloud", features[0].value)  # Whitespace collapsed and trimmed

    def test_validation_exception_handling(self) -> None:
        """Validator raises ValueError when required fields are missing or threshold is not met."""
        entity = ExtractedEntity(
            entity_type="SKILL",
            value="Python",
            confidence=0.4,  # Below threshold
            location=EntityLocation(segment_id="seg_1", start_char=0, end_char=6),
            metadata={"skill_id": "SKL-01"},
        )
        canonical = self._create_mock_canonical([entity])
        rules = {
            "skill_feature_rules": {
                "confidence_threshold": 0.5,
            }
        }
        context = FeatureExtractionContext(
            correlation_id="test_corr_val_fail",
            rule_engine_config=rules,
        )

        with self.assertRaises(ValueError):
            self._extractor.extract(canonical, context)

    def test_empty_skill_collection_handling(self) -> None:
        """Extractor handles empty collections and returns empty arrays gracefully."""
        canonical = self._create_mock_canonical([])
        context = FeatureExtractionContext(correlation_id="test_corr_empty")
        features = self._extractor.extract(canonical, context)
        self.assertEqual(0, len(features))

    def test_registry_and_pipeline_integration(self) -> None:
        """E2E pipeline integrates and runs dynamically registered SkillFeatureExtractor successfully."""
        self._service.registry.register("skill_features", SkillFeatureExtractor)

        entity = ExtractedEntity(
            entity_type="SKILL",
            value="Docker",
            confidence=0.9,
            location=EntityLocation(segment_id="seg_1", start_char=0, end_char=6),
            metadata={"skill_id": "SKL-02"},
        )
        canonical = self._create_mock_canonical([entity])

        collection = self._service.extract_features(
            canonical,
            enabled_extractors=["skill_features"],
        )

        self.assertEqual(1, len(collection.features))
        self.assertEqual("FEAT-SKILL-SKL-02", collection.features[0].feature_id)
        self.assertIn("SkillFeatureExtractor", collection.statistics.extractor_counts)

    def test_thread_safety_under_concurrent_extractions(self) -> None:
        """Extractor executes concurrently without shared mutable state failures."""
        entity = ExtractedEntity(
            entity_type="SKILL",
            value="Python",
            confidence=0.9,
            location=EntityLocation(segment_id="seg_1", start_char=0, end_char=6),
            metadata={"skill_id": "SKL-01"},
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
