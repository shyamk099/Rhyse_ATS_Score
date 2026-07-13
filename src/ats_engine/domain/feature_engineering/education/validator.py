"""Validation engine for Education features.

Purpose:
    Ensure education entity integrity, validate identifiers,
    and report warnings for missing fields or thresholds.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.education.education_models import EducationEntity
from ats_engine.domain.feature_engineering.education.rules import EducationFeatureRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class EducationFeatureValidator:
    """Validator enforcing integrity checks and emitting warnings for raw/non-canonical data."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(self, entity: EducationEntity, rules: EducationFeatureRules) -> list[str]:
        """Perform checks on an Education entity.

        Args:
            entity: The EducationEntity being evaluated.
            rules: Active EducationFeatureRules payload.

        Returns:
            A list of warning messages generated during validation.

        Raises:
            ValueError: If a required field is missing or validation fails strictly.
        """
        warnings: list[str] = []

        # 1. Required fields check
        required: Sequence[str] = rules.required_fields
        if "institution" in required and not entity.institution_name:
            raise ValueError("Required education feature field 'institution' is missing.")
        if "degree" in required and not entity.degree:
            raise ValueError("Required education feature field 'degree' is missing.")

        # 2. Canonical ID format and validation warnings (Refinement 4)
        education_id = entity.education_id
        if not education_id:
            msg = "Education entity has no education ID."
            self._logger.warning(
                "education_validation_missing_id",
                extra={"institution_name": entity.institution_name, "warning": msg},
            )
            warnings.append(msg)
        elif not education_id.startswith("EDU-"):
            msg = f"Education ID '{education_id}' does not conform to expected 'EDU-' prefix."
            self._logger.warning(
                "education_validation_invalid_id_prefix",
                extra={"education_id": education_id, "warning": msg},
            )
            warnings.append(msg)

        # 3. Confidence range validation
        if entity.confidence < rules.confidence_threshold:
            raise ValueError(
                f"Education confidence {entity.confidence} is below "
                f"configured threshold of {rules.confidence_threshold}."
            )

        # 4. Provenance check
        if not entity.source_segment_ids:
            msg = f"Education entity '{education_id}' is missing physical provenance segment IDs."
            self._logger.warning(
                "education_validation_missing_provenance",
                extra={"education_id": education_id, "warning": msg},
            )
            warnings.append(msg)

        return warnings
