"""Project extraction coordination service.

Purpose:
    Expose a unified service interface to run compound project extraction
    on a CanonicalDocument and SectionCollection.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.project.pipeline import ProjectExtractionPipeline
from ats_engine.domain.entity_extraction.section.section_models import SectionCollection
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ProjectExtractionService:
    """Service driving compound project parsing from document sections."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize service with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def extract_project(
        self,
        document: CanonicalDocument,
        sections: SectionCollection,
        rule_engine_config: Mapping[str, Any] | None = None,
    ) -> ProjectCollection:
        """Scan canonical document sections and extract structured project records.

        Args:
            document: The CanonicalDocument contract.
            sections: The SectionCollection logical grouping.
            rule_engine_config: Rule configurations from the Rule Engine.

        Returns:
            The compiled ProjectCollection.
        """
        self._logger.info(
            "project_extraction_started",
            extra={"canonical_id": document.canonical_id},
        )

        rules_payload = (rule_engine_config or {}).get("project_extraction_rules")
        if isinstance(rules_payload, dict):
            rules = ProjectExtractionRules(**rules_payload)
        else:
            rules = ProjectExtractionRules()

        collection = ProjectExtractionPipeline.execute(document, sections, rules)

        self._logger.info(
            "project_extraction_completed",
            extra={
                "canonical_id": document.canonical_id,
                "total_projects": collection.statistics.total_projects,
                "with_repo": collection.statistics.projects_with_repo,
                "with_demo": collection.statistics.projects_with_demo,
                "duration_seconds": collection.statistics.execution_duration_seconds,
            },
        )

        return collection
