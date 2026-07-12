"""Experience extraction coordination service.

Purpose:
    Expose a unified service interface to run compound experience extraction
    on a CanonicalDocument and SectionCollection.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules
from ats_engine.domain.entity_extraction.experience.pipeline import ExperienceExtractionPipeline
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ExperienceExtractionService:
    """Service driving compound experience parsing from document sections."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract_experience(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> ExperienceCollection:
        """Scan canonical document sections and extract structured experience records.

        Args:
            document: The CanonicalDocument contract.
            sections: The SectionCollection logical grouping.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled ExperienceCollection.
        """
        self._logger.info(
            "experience_extraction_started",
            extra={"canonical_id": document.canonical_id},
        )

        rules_payload = (rule_engine_config or {}).get("experience_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = ExperienceExtractionRules(**rules_payload)
        else:
            rules = ExperienceExtractionRules()

        collection = ExperienceExtractionPipeline.execute(document, sections, rules)

        self._logger.info(
            "experience_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_experiences": collection.statistics.total_experiences,
                "current_count": collection.statistics.current_employment_count,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
