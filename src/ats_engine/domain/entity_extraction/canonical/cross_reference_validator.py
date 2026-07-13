"""Cross-reference validator.

Purpose:
    Validate that referenced canonical Skill IDs exist within the extracted
    SkillCollection. Prevents broken references.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import ValidationErrorDetail
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.canonical.exceptions import CrossReferenceValidationError
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection


class CrossReferenceValidator:
    """Stateless validator verifying cross-collection entity references."""

    @classmethod
    def validate(
        cls,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        rules: CanonicalValidationRules,
    ) -> Sequence[ValidationErrorDetail]:
        """Verify referenced Skill IDs exist in SkillCollection.

        Args:
            skills: Skill collection containing extracted Skill IDs.
            experiences: Experience collection.
            projects: Project collection.
            certifications: Certification collection.
            rules: Validation rules.

        Returns:
            A sequence of ValidationErrorDetail representing issues found.

        Raises:
            CrossReferenceValidationError: If strict validation is enabled and references are broken.
        """
        errors: list[ValidationErrorDetail] = []

        # Build set of all extracted Skill IDs
        extracted_skill_ids = set()
        for e in skills.entities:
            sid = e.metadata.get("skill_id")
            if sid:
                extracted_skill_ids.add(sid)

        # 1. Check Projects
        for proj in projects.entities:
            for tech in proj.technologies:
                if tech.skill_id and tech.skill_id not in extracted_skill_ids:
                    msg = f"Project technology references missing Skill ID: {tech.skill_id}"
                    if rules.strict_cross_referencing:
                        raise CrossReferenceValidationError(msg)
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=proj.project_id,
                            entity_type="Project",
                            field_name="technologies",
                            error_message=msg,
                            severity="ERROR",
                        )
                    )

        # 2. Check Certifications
        for cert in certifications.entities:
            for sid in cert.associated_skill_ids:
                if sid not in extracted_skill_ids:
                    msg = f"Certification references missing Skill ID: {sid}"
                    if rules.strict_cross_referencing:
                        raise CrossReferenceValidationError(msg)
                    errors.append(
                        ValidationErrorDetail(
                            entity_id=cert.certification_id,
                            entity_type="Certification",
                            field_name="associated_skill_ids",
                            error_message=msg,
                            severity="ERROR",
                        )
                    )

        return errors
