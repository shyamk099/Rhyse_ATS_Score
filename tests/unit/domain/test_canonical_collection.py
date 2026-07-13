"""Unit tests for the Canonical Entity Collection and Validation pipeline.

Purpose:
    Verify CanonicalEntityCollection construction, structural validation check,
    duplicate resolution strategies, cross-reference checks, URL validation,
    provenance validation, statistics generation, and exception handling.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.entity_extraction.canonical.canonical_models import (
    CanonicalEntityCollection,
    ValidationErrorDetail,
    ValidationSummary,
)
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.canonical.exceptions import (
    CrossReferenceValidationError,
    EntityValidationError,
)
from ats_engine.domain.entity_extraction.canonical.service import CanonicalEntityCollectionService
from ats_engine.domain.entity_extraction.models import EntityCollection, ExtractedEntity, EntityLocation, EntityExtractionStatistics
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.skills.skill_models import SkillExtractionStatistics
from ats_engine.domain.entity_extraction.experience.experience_models import (
    ExperienceCollection,
    ExperienceEntity,
    ExperienceExtractionStatistics,
)
from ats_engine.domain.entity_extraction.education.education_models import (
    EducationCollection,
    EducationEntity,
    EducationExtractionStatistics,
)
from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectCollection,
    ProjectEntity,
    ProjectExtractionStatistics,
    ProjectTechnology,
    ProjectURL,
)
from ats_engine.domain.entity_extraction.certification.certification_models import (
    CertificationCollection,
    CertificationEntity,
    CertificationExtractionStatistics,
    CertificationURL,
)


class CanonicalEntityCollectionTests(unittest.TestCase):
    """Test suite validating canonical collection validation and deduplication."""

    def setUp(self) -> None:
        """Initialize the canonical entity collection service."""
        self._service = CanonicalEntityCollectionService()

    def test_builds_valid_collection(self) -> None:
        """Pipeline successfully constructs an immutable CanonicalEntityCollection with stats."""
        contacts = EntityCollection(
            entities=(
                ExtractedEntity(
                    entity_type="email",
                    value="test@example.com",
                    confidence=0.9,
                    location=EntityLocation(segment_id="seg-01", start_char=0, end_char=16),
                ),
            ),
            statistics=EntityExtractionStatistics(
                total_entities=1,
                execution_duration_seconds=0.01,
            )
        )
        skills = SkillCollection(
            entities=(
                ExtractedEntity(
                    entity_type="Skill",
                    value="Python",
                    confidence=0.95,
                    location=EntityLocation(segment_id="seg-02", start_char=0, end_char=6),
                    metadata={"skill_id": "SKL-01"},
                ),
            ),
            statistics=SkillExtractionStatistics(
                total_skills_found=1,
                unique_skills_count=1,
                execution_duration_seconds=0.01,
            ),
        )
        experiences = ExperienceCollection(
            entities=(
                ExperienceEntity(
                    experience_id="EXP-00000001",
                    company_name="Acme Corp",
                    job_title="Software Engineer",
                    start_date_raw="2020",
                    end_date_raw="2022",
                    confidence=0.9,
                ),
            ),
            statistics=ExperienceExtractionStatistics(
                total_experiences=1,
                current_employment_count=0,
                execution_duration_seconds=0.01,
            ),
        )
        education = EducationCollection(
            entities=(
                EducationEntity(
                    education_id="EDU-00000001",
                    institution_name="MIT",
                    degree="BS",
                    confidence=0.9,
                ),
            ),
            statistics=EducationExtractionStatistics(
                total_education_records=1,
                records_with_degree=1,
                records_with_gpa=0,
                execution_duration_seconds=0.01,
            ),
        )
        projects = ProjectCollection(
            entities=(
                ProjectEntity(
                    project_id="PROJ-00000001",
                    project_name="Web Crawler",
                    technologies=(
                        ProjectTechnology(raw_name="Python", skill_id="SKL-01"),
                    ),
                    confidence=0.9,
                ),
            ),
            statistics=ProjectExtractionStatistics(
                total_projects=1,
                projects_with_repo=0,
                projects_with_demo=0,
                execution_duration_seconds=0.01,
            ),
        )
        certifications = CertificationCollection(
            entities=(
                CertificationEntity(
                    certification_id="CERT-00000001",
                    certification_name="AWS Architect",
                    associated_skill_ids=("SKL-01",),
                    confidence=0.9,
                ),
            ),
            statistics=CertificationExtractionStatistics(
                total_certifications=1,
                active_certifications=1,
                execution_duration_seconds=0.01,
            ),
        )

        collection = self._service.build(
            contacts=contacts,
            skills=skills,
            experiences=experiences,
            education=education,
            projects=projects,
            certifications=certifications,
        )

        self.assertIsInstance(collection, CanonicalEntityCollection)
        self.assertEqual("VALID", collection.validation_summary.status)
        self.assertEqual(1, collection.statistics.contact_count)
        self.assertEqual(1, collection.statistics.skill_count)

    def test_broken_skill_references_strict(self) -> None:
        """Pipeline raises CrossReferenceValidationError if strict cross referencing is enabled and references are broken."""
        contacts = EntityCollection(entities=(), statistics=EntityExtractionStatistics(total_entities=0, execution_duration_seconds=0.0))
        skills = SkillCollection(
            entities=(),
            statistics=SkillExtractionStatistics(
                total_skills_found=0, unique_skills_count=0, execution_duration_seconds=0.0
            ),
        )
        experiences = ExperienceCollection(entities=(), statistics=ExperienceExtractionStatistics(total_experiences=0, current_employment_count=0, execution_duration_seconds=0.0))
        education = EducationCollection(entities=(), statistics=EducationExtractionStatistics(total_education_records=0, records_with_degree=0, records_with_gpa=0, execution_duration_seconds=0.0))
        
        # References "SKL-99" which is not in skills collection
        projects = ProjectCollection(
            entities=(
                ProjectEntity(
                    project_id="PROJ-00000001",
                    project_name="Web Crawler",
                    technologies=(
                        ProjectTechnology(raw_name="Python", skill_id="SKL-99"),
                    ),
                    confidence=0.9,
                ),
            ),
            statistics=ProjectExtractionStatistics(total_projects=1, projects_with_repo=0, projects_with_demo=0, execution_duration_seconds=0.01),
        )
        certifications = CertificationCollection(entities=(), statistics=CertificationExtractionStatistics(total_certifications=0, active_certifications=0, execution_duration_seconds=0.0))

        rules = {
            "canonical_validation_rules": {
                "strict_cross_referencing": True,
            }
        }

        with self.assertRaises(CrossReferenceValidationError):
            self._service.build(
                contacts=contacts,
                skills=skills,
                experiences=experiences,
                education=education,
                projects=projects,
                certifications=certifications,
                rule_engine_config=rules,
            )

    def test_duplicate_resolution_keeps_highest_confidence(self) -> None:
        """Pipeline resolves duplicate experience IDs keeping the one with higher confidence."""
        contacts = EntityCollection(entities=(), statistics=EntityExtractionStatistics(total_entities=0, execution_duration_seconds=0.0))
        skills = SkillCollection(
            entities=(),
            statistics=SkillExtractionStatistics(
                total_skills_found=0, unique_skills_count=0, execution_duration_seconds=0.0
            ),
        )
        
        # Two experiences with identical ID but different confidence
        experiences = ExperienceCollection(
            entities=(
                ExperienceEntity(
                    experience_id="EXP-00000001",
                    company_name="Acme Corp",
                    job_title="Software Engineer",
                    confidence=0.5,
                ),
                ExperienceEntity(
                    experience_id="EXP-00000001",
                    company_name="Acme Corp",
                    job_title="Software Engineer",
                    confidence=0.9,
                ),
            ),
            statistics=ExperienceExtractionStatistics(
                total_experiences=2,
                current_employment_count=0,
                execution_duration_seconds=0.01,
            ),
        )
        education = EducationCollection(entities=(), statistics=EducationExtractionStatistics(total_education_records=0, records_with_degree=0, records_with_gpa=0, execution_duration_seconds=0.0))
        projects = ProjectCollection(entities=(), statistics=ProjectExtractionStatistics(total_projects=0, projects_with_repo=0, projects_with_demo=0, execution_duration_seconds=0.0))
        certifications = CertificationCollection(entities=(), statistics=CertificationExtractionStatistics(total_certifications=0, active_certifications=0, execution_duration_seconds=0.0))

        collection = self._service.build(
            contacts=contacts,
            skills=skills,
            experiences=experiences,
            education=education,
            projects=projects,
            certifications=certifications,
        )

        self.assertEqual(1, len(collection.experiences.entities))
        self.assertEqual(0.9, collection.experiences.entities[0].confidence)
        self.assertEqual(1, collection.validation_summary.duplicate_count)

    def test_malformed_urls_trigger_validation_failure(self) -> None:
        """Pipeline marks collection invalid and reports validation errors if URL is malformed."""
        contacts = EntityCollection(entities=(), statistics=EntityExtractionStatistics(total_entities=0, execution_duration_seconds=0.0))
        skills = SkillCollection(
            entities=(),
            statistics=SkillExtractionStatistics(
                total_skills_found=0, unique_skills_count=0, execution_duration_seconds=0.0
            ),
        )
        experiences = ExperienceCollection(entities=(), statistics=ExperienceExtractionStatistics(total_experiences=0, current_employment_count=0, execution_duration_seconds=0.0))
        education = EducationCollection(entities=(), statistics=EducationExtractionStatistics(total_education_records=0, records_with_degree=0, records_with_gpa=0, execution_duration_seconds=0.0))
        
        # Project has malformed repo URL
        projects = ProjectCollection(
            entities=(
                ProjectEntity(
                    project_id="PROJ-00000001",
                    project_name="Web Crawler",
                    repo_url=ProjectURL(
                        original_value="not_a_valid_url",
                        normalized_value="not_a_valid_url",
                        matched_rule="github",
                    ),
                    confidence=0.9,
                ),
            ),
            statistics=ProjectExtractionStatistics(total_projects=1, projects_with_repo=1, projects_with_demo=0, execution_duration_seconds=0.01),
        )
        certifications = CertificationCollection(entities=(), statistics=CertificationExtractionStatistics(total_certifications=0, active_certifications=0, execution_duration_seconds=0.0))

        rules = {
            "canonical_validation_rules": {
                "required_collections": [],
            }
        }

        collection = self._service.build(
            contacts=contacts,
            skills=skills,
            experiences=experiences,
            education=education,
            projects=projects,
            certifications=certifications,
            rule_engine_config=rules,
        )

        self.assertEqual("INVALID", collection.validation_summary.status)
        self.assertTrue(len(collection.validation_summary.errors) > 0)
        self.assertIn("Malformed repository URL", collection.validation_summary.errors[0].error_message)
