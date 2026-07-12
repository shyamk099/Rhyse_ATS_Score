"""Education extraction coordination service.

Purpose:
    Expose a unified service interface to run compound education extraction
    on a CanonicalDocument and SectionCollection.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules
from ats_engine.domain.entity_extraction.education.pipeline import EducationExtractionPipeline
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.infrastructure.logging.factory import LoggerFactory


class EducationExtractionService:
    """Service driving compound education parsing from document sections."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract_education(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> EducationCollection:
        """Scan canonical document sections and extract structured education records.

        Args:
            document: The CanonicalDocument contract.
            sections: The SectionCollection logical grouping.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled EducationCollection.
        """
        self._logger.info(
            "education_extraction_started",
            extra={"canonical_id": document.canonical_id},
        )

        rules_payload = (rule_engine_config or {}).get("education_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = EducationExtractionRules(**rules_payload)
        else:
            rules = EducationExtractionRules()

        collection = EducationExtractionPipeline.execute(document, sections, rules)

        self._logger.info(
            "education_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_records": collection.statistics.total_education_records,
                "with_degree": collection.statistics.records_with_degree,
                "with_gpa": collection.statistics.records_with_gpa,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
