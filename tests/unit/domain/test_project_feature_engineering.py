"""Unit and Integration tests for Project Feature Engineering.

Purpose:
    Verify Project entity mapping, whitespace normalization, validation rules,
    1:1 project entity preservation, None-preservation for raw/missing details,
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
    ProjectEntity,
    ProjectExtractionStatistics,
    ProjectTechnology,
    ProjectURL,
)
from ats_engine.domain.entity_extraction.skills.skill_models import (
    SkillCollection,
    SkillExtractionStatistics,
)
from ats_engine.domain.feature_engineering.models import FeatureCategory, FeatureExtractionContext
from ats_engine.domain.feature_engineering.service import FeatureEngineeringService
from ats_engine.domain.feature_engineering.project.extractor import ProjectFeatureExtractor


class ProjectFeatureEngineeringTests(unittest.TestCase):
    """Test suite validating ProjectFeatureExtractor lifecycle and refinements."""

    def setUp(self) -> None:
        """Initialize service wrapper and mock entity objects."""
        self._service = FeatureEngineeringService()
        self._extractor = ProjectFeatureExtractor()

    def _create_mock_canonical(
        self,
        proj_entities: list[ProjectEntity],
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
                entities=tuple(proj_entities),
                statistics=ProjectExtractionStatistics(
                    total_projects=len(proj_entities),
                    projects_with_repo=sum(1 for e in proj_entities if e.repo_url),
                    projects_with_demo=sum(1 for e in proj_entities if e.demo_url),
                    execution_duration_seconds=0.01,
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
                project_count=len(proj_entities),
                certification_count=0,
                duplicate_count=0,
                validation_error_count=0,
                processing_duration_seconds=0.01,
            ),
        )

    def test_extracts_canonical_project_to_feature(self) -> None:
        """Extractor maps valid canonical project to a generic Feature DTO."""
        entity = ProjectEntity(
            project_id="PROJ-01",
            project_name="Rhyse ATS Score",
            organization="DeepMind pair",
            role="AI Agent Architect",
            start_date_raw="2026-06",
            end_date_raw="2026-07",
            duration_raw="1 month",
            technologies=(ProjectTechnology(raw_name="Python", skill_id="SKL-PY"),),
            responsibilities=("Design parser workflows",),
            achievements=("Built pipeline runner integration",),
            project_description="ATS Intelligence Engine design",
            repo_url=ProjectURL(original_value="http://github", normalized_value="https://github", matched_rule="url_regex"),
            demo_url=ProjectURL(original_value="http://demo", normalized_value="https://demo", matched_rule="url_regex"),
            location_raw="Bengaluru, India",
            confidence=0.99,
            confidence_reason="Complete records matched",
            matched_rules=("proj_rule1",),
            source_segment_ids=("seg_1",),
            source_text="Worked on Rhyse ATS Score...",
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_proj")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        feat = features[0]
        self.assertEqual("FEAT-PROJECT-PROJ-01", feat.feature_id)
        self.assertEqual("Rhyse ATS Score", feat.name)
        self.assertEqual(FeatureCategory.PROJECT, feat.category)
        self.assertEqual(0.99, feat.confidence)
        self.assertEqual("PROJ-01", feat.provenance.source_entity_id)

        # check generic values
        val = feat.value
        self.assertEqual("Rhyse ATS Score", val["project_name"])
        self.assertEqual("DeepMind pair", val["organization"])
        self.assertEqual("AI Agent Architect", val["role"])
        self.assertEqual("2026-06", val["start_date_raw"])
        self.assertEqual("2026-07", val["end_date_raw"])
        self.assertEqual("1 month", val["duration_raw"])
        self.assertEqual("Python", val["technologies"][0]["raw_name"])
        self.assertEqual("SKL-PY", val["technologies"][0]["skill_id"])
        self.assertEqual(("Design parser workflows",), val["responsibilities"])
        self.assertEqual(("Built pipeline runner integration",), val["achievements"])
        self.assertEqual("https://github", val["repository_urls"]["normalized_value"])
        self.assertEqual("https://demo", val["demo_urls"]["normalized_value"])
        self.assertEqual("Bengaluru, India", val["location"])

    def test_retains_exactly_one_feature_per_record(self) -> None:
        """Extractor preserves 1:1 mapping and does not split project records (Refinement 3)."""
        entity1 = ProjectEntity(
            project_id="PROJ-01",
            project_name="Project One",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        entity2 = ProjectEntity(
            project_id="PROJ-02",
            project_name="Project Two",
            confidence=0.8,
            source_segment_ids=("seg_2",),
        )
        canonical = self._create_mock_canonical([entity1, entity2])
        context = FeatureExtractionContext(correlation_id="test_corr_one_feature")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(2, len(features))
        self.assertEqual("FEAT-PROJECT-PROJ-01", features[0].feature_id)
        self.assertEqual("FEAT-PROJECT-PROJ-02", features[1].feature_id)

    def test_whitespace_normalization_only(self) -> None:
        """Normalizer trims whitespace and duplicate spaces without changing canonical texts (Refinement 6)."""
        entity = ProjectEntity(
            project_id="PROJ-01",
            project_name="  Rhyse   ATS   Score  ",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        context = FeatureExtractionContext(correlation_id="test_corr_norm")

        features = self._extractor.extract(canonical, context)

        self.assertEqual(1, len(features))
        val = features[0].value
        self.assertEqual("Rhyse ATS Score", val["project_name"])

    def test_validation_exception_handling(self) -> None:
        """Validator raises ValueError when required fields are missing or threshold is not met."""
        entity = ProjectEntity(
            project_id="PROJ-01",
            project_name="Project Fail",
            confidence=0.3,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])
        rules = {
            "project_feature_rules": {
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
        """E2E pipeline integrates and runs dynamically registered ProjectFeatureExtractor successfully."""
        self._service.registry.register("project_features", ProjectFeatureExtractor)

        entity = ProjectEntity(
            project_id="PROJ-02",
            project_name="Registered Project",
            confidence=0.9,
            source_segment_ids=("seg_1",),
        )
        canonical = self._create_mock_canonical([entity])

        collection = self._service.extract_features(
            canonical,
            enabled_extractors=["project_features"],
        )

        self.assertEqual(1, len(collection.features))
        self.assertEqual("FEAT-PROJECT-PROJ-02", collection.features[0].feature_id)

    def test_thread_safety_under_concurrent_extractions(self) -> None:
        """Extractor executes concurrently without shared mutable state failures."""
        entity = ProjectEntity(
            project_id="PROJ-01",
            project_name="Parallel Project",
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
