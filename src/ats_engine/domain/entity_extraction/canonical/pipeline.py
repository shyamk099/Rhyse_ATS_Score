"""Canonical entity collection builder pipeline.

Purpose:
    Coordinate validation stages, duplicate resolution, and build the final
    immutable CanonicalEntityCollection.
"""

from __future__ import annotations

import time
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import (
    CanonicalEntityCollection,
    EntityStatistics,
    ValidationErrorDetail,
    ValidationSummary,
)
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.canonical.entity_validator import EntityValidator
from ats_engine.domain.entity_extraction.canonical.duplicate_resolver import DuplicateResolver
from ats_engine.domain.entity_extraction.canonical.cross_reference_validator import CrossReferenceValidator
from ats_engine.domain.entity_extraction.models import EntityCollection
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection


class CanonicalEntityCollectionPipeline:
    """Stateless pipeline building and validating the CanonicalEntityCollection."""

    @classmethod
    def execute(
        cls,
        contacts: EntityCollection,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        education: EducationCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        rules: CanonicalValidationRules,
    ) -> CanonicalEntityCollection:
        """Run validation -> deduplicate -> cross reference -> compile.

        Args:
            contacts: Extracted contacts.
            skills: Extracted skills.
            experiences: Extracted experiences.
            education: Extracted education.
            projects: Extracted projects.
            certifications: Extracted certifications.
            rules: Validation rules.

        Returns:
            The immutable CanonicalEntityCollection.
        """
        start_time = time.perf_counter()

        # 1. Structural Validation
        errors = list(
            EntityValidator.validate(
                contacts, skills, experiences, education, projects, certifications, rules
            )
        )

        # 2. Duplicate Resolution
        deduped_experiences = DuplicateResolver.resolve(
            experiences.entities, rules, key_field="experience_id"
        )
        deduped_education = DuplicateResolver.resolve(
            education.entities, rules, key_field="education_id"
        )
        deduped_projects = DuplicateResolver.resolve(
            projects.entities, rules, key_field="project_id"
        )
        deduped_certifications = DuplicateResolver.resolve(
            certifications.entities, rules, key_field="certification_id"
        )

        # Calculate duplicate count
        original_count = (
            len(experiences.entities)
            + len(education.entities)
            + len(projects.entities)
            + len(certifications.entities)
        )
        deduped_count = (
            len(deduped_experiences)
            + len(deduped_education)
            + len(deduped_projects)
            + len(deduped_certifications)
        )
        duplicate_count = original_count - deduped_count

        # Re-build collections with deduplicated entities
        clean_experiences = ExperienceCollection(
            entities=tuple(deduped_experiences),
            statistics=experiences.statistics,
        )
        clean_education = EducationCollection(
            entities=tuple(deduped_education),
            statistics=education.statistics,
        )
        clean_projects = ProjectCollection(
            entities=tuple(deduped_projects),
            statistics=projects.statistics,
        )
        clean_certifications = CertificationCollection(
            entities=tuple(deduped_certifications),
            statistics=certifications.statistics,
        )

        # 3. Cross-Reference Validation
        xref_errors = CrossReferenceValidator.validate(
            skills, clean_experiences, clean_projects, clean_certifications, rules
        )
        errors.extend(xref_errors)

        # 4. Build Validation Summary
        is_valid = not any(err.severity == "ERROR" for err in errors)
        status = "VALID" if is_valid else "INVALID"

        validation_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rules_version = "canonical_validation_rules:1.0"

        validation_summary = ValidationSummary(
            status=status,
            errors=tuple(err for err in errors if err.severity == "ERROR"),
            warnings=tuple(err for err in errors if err.severity == "WARNING"),
            duplicate_count=duplicate_count,
            reference_errors=len(xref_errors),
            validation_timestamp=validation_timestamp,
            rules_version=rules_version,
        )

        # 5. Build Aggregated Statistics
        duration = time.perf_counter() - start_time
        stats = cls._build_statistics(
            contacts,
            skills,
            clean_experiences,
            clean_education,
            clean_projects,
            clean_certifications,
            duplicate_count,
            len(validation_summary.errors),
            duration,
        )

        return CanonicalEntityCollection(
            contacts=contacts,
            skills=skills,
            experiences=clean_experiences,
            education=clean_education,
            projects=clean_projects,
            certifications=clean_certifications,
            validation_summary=validation_summary,
            statistics=stats,
        )

    @classmethod
    def _build_statistics(
        cls,
        contacts: EntityCollection,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        education: EducationCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        duplicate_count: int,
        error_count: int,
        duration: float,
    ) -> EntityStatistics:
        """Aggregate extraction statistics across all modules."""
        return EntityStatistics(
            contact_count=len(contacts.entities),
            skill_count=len(skills.entities),
            experience_count=len(experiences.entities),
            education_count=len(education.entities),
            project_count=len(projects.entities),
            certification_count=len(certifications.entities),
            duplicate_count=duplicate_count,
            validation_error_count=error_count,
            processing_duration_seconds=duration,
        )
