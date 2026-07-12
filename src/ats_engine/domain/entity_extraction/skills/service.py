"""Skill extraction coordination service.

Purpose:
    Expose a unified service interface to run dictionary-driven skill extraction
    on a CanonicalDocument and SectionCollection.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.domain.entity_extraction.skills.pipeline import SkillExtractionPipeline
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.skills.skill_rules import SkillExtractionRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SkillExtractionService:
    """Service driving candidate scanning, validation, normalization, and filters."""

    def __init__(
        self,
        pipeline: SkillExtractionPipeline | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """Initialize service with optional pipeline and logger dependencies."""
        self._pipeline = pipeline or SkillExtractionPipeline()
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract_skills(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> SkillCollection:
        """Scan canonical document segments and extract structured skills taxonomy details.

        Args:
            document: The CanonicalDocument contract.
            sections: The SectionCollection logical grouping.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled SkillCollection.
        """
        self._logger.info("skill_extraction_started", extra={"canonical_id": document.canonical_id})

        # Resolve rules payload from Rule Engine config
        rules_payload = (rule_engine_config or {}).get("skill_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = SkillExtractionRules(**rules_payload)
        else:
            rules = SkillExtractionRules()

        collection = self._pipeline.execute(document, sections, rules)

        self._logger.info(
            "skill_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_skills": collection.statistics.total_skills_found,
                "unique_skills": collection.statistics.unique_skills_count,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
