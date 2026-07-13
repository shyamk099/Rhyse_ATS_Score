"""Canonical Entity Collection coordination service.

Purpose:
    Expose a unified service interface to build and validate the consolidated
    CanonicalEntityCollection contract.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules
from ats_engine.domain.entity_extraction.canonical.pipeline import CanonicalEntityCollectionPipeline
from ats_engine.domain.entity_extraction.models import EntityCollection
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CanonicalEntityCollectionService:
    """Service consolidating and validating all extracted entities into the final Book 03 output contract."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def build(
        self,
        contacts: EntityCollection,
        skills: SkillCollection,
        experiences: ExperienceCollection,
        education: EducationCollection,
        projects: ProjectCollection,
        certifications: CertificationCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> CanonicalEntityCollection:
        """Validate and construct the CanonicalEntityCollection output.

        Args:
            contacts: Extracted contacts.
            skills: Extracted skills.
            experiences: Extracted experiences.
            education: Extracted education.
            projects: Extracted projects.
            certifications: Extracted certifications.
            rule_engine_config: Config options from the Rule Engine.

        Returns:
            The validated CanonicalEntityCollection.
        """
        self._logger.info("canonical_entity_collection_build_started")

        rules_payload = (rule_engine_config or {}).get("canonical_validation_rules")
        if isinstance(rules_payload, dict):
            rules = CanonicalValidationRules(**rules_payload)
        else:
            rules = CanonicalValidationRules()

        collection = CanonicalEntityCollectionPipeline.execute(
            contacts=contacts,
            skills=skills,
            experiences=experiences,
            education=education,
            projects=projects,
            certifications=certifications,
            rules=rules,
        )

        self._logger.info(
            "canonical_entity_collection_build_completed",
            extra={
                "total_entities": collection.statistics.contact_count
                + collection.statistics.skill_count
                + collection.statistics.experience_count
                + collection.statistics.education_count
                + collection.statistics.project_count
                + collection.statistics.certification_count,
                "is_valid": collection.validation_summary.status == "VALID",
                "errors_count": len(collection.validation_summary.errors),
                "warnings_count": len(collection.validation_summary.warnings),
            },
        )

        return collection
