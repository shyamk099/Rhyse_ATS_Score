"""Entity validator.

Purpose:
    Validate structural integrity: verify segment boundaries, offsets,
    malformed URLs, and empty collections.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import ValidationErrorDetail
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.models import EntityCollection
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection


class EntityValidator:
    """Stateless validator checking structural integrity of all extracted entities."""

    @classmethod
    def validate(
        cls,
        contacts: EntityCollection,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        education: EducationCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        rules: CanonicalValidationRules,
    ) -> Sequence[ValidationErrorDetail]:
        """Validate structural integrity of collections.

        Args:
            contacts: Extracted contacts.
            skills: Extracted skills.
            experiences: Extracted experiences.
            education: Extracted education.
            projects: Extracted projects.
            certifications: Extracted certifications.
            rules: Validation rules.

        Returns:
            A sequence of ValidationErrorDetail representing issues found.
        """
        errors: list[ValidationErrorDetail] = []

        # 1. Check for empty required collections
        if "contacts" in rules.required_collections and not contacts.entities:
            errors.append(
                ValidationErrorDetail(
                    entity_id="SYSTEM",
                    entity_type="EntityCollection",
                    field_name="entities",
                    error_message="Required contact collection is empty",
                    severity="ERROR",
                )
            )

        if "skills" in rules.required_collections and not skills.entities:
            errors.append(
                ValidationErrorDetail(
                    entity_id="SYSTEM",
                    entity_type="SkillCollection",
                    field_name="entities",
                    error_message="Required skill collection is empty",
                    severity="ERROR",
                )
            )

        # 2. Check for duplicate IDs across all collections
        all_ids = set()
        
        # Helper to check duplicate IDs
        def _check_ids(entities, etype):
            for e in entities:
                eid = getattr(e, "experience_id", None) or getattr(e, "education_id", None) or getattr(e, "project_id", None) or getattr(e, "certification_id", None) or getattr(e, "entity_id", None)
                if eid:
                    if eid in all_ids:
                        errors.append(
                            ValidationErrorDetail(
                                entity_id=eid,
                                entity_type=etype,
                                field_name="id",
                                error_message=f"Duplicate entity ID detected: {eid}",
                                severity="ERROR",
                            )
                        )
                    all_ids.add(eid)

        _check_ids(contacts.entities, "Contact")
        _check_ids(skills.entities, "Skill")
        _check_ids(experiences.entities, "Experience")
        _check_ids(education.entities, "Education")
        _check_ids(projects.entities, "Project")
        _check_ids(certifications.entities, "Certification")

        # 3. Check URL formats if enabled
        if rules.validate_url_formats:
            # Check project URLs
            for proj in projects.entities:
                if proj.repo_url and not cls._is_valid_url(proj.repo_url.original_value):
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=proj.project_id,
                            entity_type="Project",
                            field_name="repo_url",
                            error_message=f"Malformed repository URL: {proj.repo_url.original_value}",
                            severity="ERROR",
                        )
                    )
                if proj.demo_url and not cls._is_valid_url(proj.demo_url.original_value):
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=proj.project_id,
                            entity_type="Project",
                            field_name="demo_url",
                            error_message=f"Malformed demo URL: {proj.demo_url.original_value}",
                            severity="ERROR",
                        )
                    )

            # Check certification URLs
            for cert in certifications.entities:
                if cert.credential_url and not cls._is_valid_url(cert.credential_url.original_value):
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=cert.certification_id,
                            entity_type="Certification",
                            field_name="credential_url",
                            error_message=f"Malformed credential URL: {cert.credential_url.original_value}",
                            severity="ERROR",
                        )
                    )

        # 4. Check provenance offsets if enabled
        if rules.validate_provenance_offsets:
            for skill in skills.entities:
                loc = skill.location
                if loc and (loc.start_char < 0 or loc.end_char < loc.start_char):
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=skill.entity_id,
                            entity_type="Skill",
                            field_name="location",
                            error_message=f"Invalid character offsets: start={loc.start_char}, end={loc.end_char}",
                            severity="ERROR",
                        )
                    )

        return errors

    @classmethod
    def _is_valid_url(cls, url: str) -> bool:
        """Simple regex check for URL validation."""
        pattern = re.compile(
            r"^https?://[A-Za-z0-9.-]+(?:\.[A-Za-z]{2,})+(?:/[^\s]*)?$",
            re.IGNORECASE,
        )
        return bool(pattern.match(url))
