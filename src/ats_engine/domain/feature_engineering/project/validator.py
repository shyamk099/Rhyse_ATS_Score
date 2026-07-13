"""Validation engine for Project features.

Purpose:
    Ensure project entity integrity, validate identifiers,
    and report warnings for missing fields or thresholds.
"""

from __future__ import annotations

import logging

from ats_engine.domain.entity_extraction.project.project_models import ProjectEntity
from ats_engine.domain.feature_engineering.common.validation import (
    validate_confidence_threshold,
    validate_required_fields,
)
from ats_engine.domain.feature_engineering.project.rules import ProjectFeatureRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ProjectFeatureValidator:
    """Validator enforcing integrity checks and emitting warnings for raw/non-canonical data."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(self, entity: ProjectEntity, rules: ProjectFeatureRules) -> list[str]:
        """Perform checks on a Project entity.

        Args:
            entity: The ProjectEntity being evaluated.
            rules: Active ProjectFeatureRules payload.

        Returns:
            A list of warning messages generated during validation.

        Raises:
            ValueError: If a required field is missing or validation fails strictly.
        """
        warnings: list[str] = []

        # 1. Required fields check
        metadata_map = {
            "organization": entity.organization,
            "role": entity.role,
            "start_date_raw": entity.start_date_raw,
            "end_date_raw": entity.end_date_raw,
            "duration_raw": entity.duration_raw,
            "location": entity.location_raw,
        }
        validate_required_fields(
            entity_val=entity.project_name,
            entity_metadata=metadata_map,
            required=rules.required_fields,
            field_mappings={"project_name": "name"},
        )

        # 2. Canonical ID format and validation warnings
        project_id = entity.project_id
        if not project_id:
            msg = "Project entity has no project ID."
            self._logger.warning(
                "project_validation_missing_id",
                extra={"project_name": entity.project_name, "warning": msg},
            )
            warnings.append(msg)
        elif not project_id.startswith("PROJ-"):
            msg = f"Project ID '{project_id}' does not conform to expected 'PROJ-' prefix."
            self._logger.warning(
                "project_validation_invalid_id_prefix",
                extra={"project_id": project_id, "warning": msg},
            )
            warnings.append(msg)

        # 3. Confidence range validation
        validate_confidence_threshold(entity.confidence, rules.confidence_threshold)

        # 4. Provenance check
        if not entity.source_segment_ids:
            msg = f"Project entity '{project_id}' is missing physical provenance segment IDs."
            self._logger.warning(
                "project_validation_missing_provenance",
                extra={"project_id": project_id, "warning": msg},
            )
            warnings.append(msg)

        return warnings
