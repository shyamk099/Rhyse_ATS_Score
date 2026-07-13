"""Certification extraction coordination service.

Purpose:
    Expose a unified service interface to run compound certification extraction
    on a CanonicalDocument and SectionCollection.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules
from ats_engine.domain.entity_extraction.certification.pipeline import CertificationExtractionPipeline
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CertificationExtractionService:
    """Service driving compound certification parsing from document sections."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract_certification(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> CertificationCollection:
        """Scan canonical document sections and extract structured certification records.

        Args:
            document: The CanonicalDocument contract.
            sections: The SectionCollection logical grouping.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled CertificationCollection.
        """
        self._logger.info(
            "certification_extraction_started",
            extra={"canonical_id": document.canonical_id},
        )

        rules_payload = (rule_engine_config or {}).get("certification_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = CertificationExtractionRules(**rules_payload)
        else:
            rules = CertificationExtractionRules()

        collection = CertificationExtractionPipeline.execute(document, sections, rules)

        self._logger.info(
            "certification_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_certifications": collection.statistics.total_certifications,
                "active_certifications": collection.statistics.active_certifications,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
