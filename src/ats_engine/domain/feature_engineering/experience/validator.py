"""Validation engine for Experience features.

Purpose:
    Ensure experience entity integrity, validate identifiers,
    and report warnings for missing fields or thresholds.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceEntity
from ats_engine.domain.feature_engineering.experience.rules import ExperienceFeatureRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class ExperienceFeatureValidator:
    """Validator enforcing integrity checks and emitting warnings for raw/non-canonical data."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(self, entity: ExperienceEntity, rules: ExperienceFeatureRules) -> list[str]:
        """Perform checks on an Experience entity.

        Args:
            entity: The ExperienceEntity being evaluated.
            rules: Active ExperienceFeatureRules payload.

        Returns:
            A list of warning messages generated during validation.

        Raises:
            ValueError: If a required field is missing or validation fails strictly.
        """
        warnings: list[str] = []

        # 1. Required fields check
        required: Sequence[str] = rules.required_fields
        if "company_name" in required and not entity.company_name:
            raise ValueError("Required experience feature field 'company_name' is missing.")
        if "job_title" in required and not entity.job_title:
            raise ValueError("Required experience feature field 'job_title' is missing.")

        # 2. Canonical ID format and validation warnings (Refinement 4)
        experience_id = entity.experience_id
        if not experience_id:
            msg = "Experience entity has no experience ID."
            self._logger.warning(
                "experience_validation_missing_id",
                extra={"company_name": entity.company_name, "warning": msg},
            )
            warnings.append(msg)
        elif not experience_id.startswith("EXP-"):
            msg = f"Experience ID '{experience_id}' does not conform to expected 'EXP-' prefix."
            self._logger.warning(
                "experience_validation_invalid_id_prefix",
                extra={"experience_id": experience_id, "warning": msg},
            )
            warnings.append(msg)

        # 3. Confidence range validation
        if entity.confidence < rules.confidence_threshold:
            raise ValueError(
                f"Experience confidence {entity.confidence} is below "
                f"configured threshold of {rules.confidence_threshold}."
            )

        # 4. Provenance check
        if not entity.source_segment_ids:
            msg = f"Experience entity '{experience_id}' is missing physical provenance segment IDs."
            self._logger.warning(
                "experience_validation_missing_provenance",
                extra={"experience_id": experience_id, "warning": msg},
            )
            warnings.append(msg)

        return warnings
