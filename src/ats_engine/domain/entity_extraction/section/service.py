"""Section detection service.

Purpose:
    Expose a unified service interface to run logical section boundary detection
    on a CanonicalDocument.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.section.pipeline import SectionDetectionPipeline
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SectionDetectionService:
    """Service driving layout block scanning, validation, and boundary grouping."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize the service with optional logger."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def detect_sections(
        self,
        document: CanonicalDocument,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> SectionCollection:
        """Extract and compile physical layout sections from a CanonicalDocument.

        Args:
            document: The CanonicalDocument contract.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled SectionCollection.
        """
        self._logger.info("section_detection_started", extra={"canonical_id": document.canonical_id})

        # Resolve rules payload from Rule Engine config
        rules_payload = (rule_engine_config or {}).get("section_detection_rules")
        if isinstance(rules_payload, dict):
            rules = SectionDetectionRules(**rules_payload)
        else:
            rules = SectionDetectionRules()

        collection = SectionDetectionPipeline.execute(document, rules)

        self._logger.info(
            "section_detection_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_sections": collection.statistics.total_sections,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
