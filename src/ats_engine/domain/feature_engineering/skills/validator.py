"""Validation engine for Skill features.

Purpose:
    Ensure skill entity integrity, validate canonical identifiers,
    and report warnings for missing metadata or identifiers.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.entity_extraction.models import ExtractedEntity
from ats_engine.domain.feature_engineering.skills.rules import SkillFeatureRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class SkillFeatureValidator:
    """Validator enforcing integrity checks and emitting warnings for raw/non-canonical data."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(self, entity: ExtractedEntity, rules: SkillFeatureRules) -> list[str]:
        """Perform checks on a Canonical Skill entity.

        Args:
            entity: The ExtractedEntity being evaluated.
            rules: Active SkillFeatureRules payload.

        Returns:
            A list of warning messages generated during validation.

        Raises:
            ValueError: If a required field is missing or validation fails strictly.
        """
        warnings: list[str] = []

        # 1. Required fields check
        required: Sequence[str] = rules.required_fields
        if "value" in required and not entity.value.strip():
            raise ValueError("Required skill feature field 'value' is empty or missing.")

        skill_id = entity.metadata.get("skill_id")
        if "skill_id" in required and not skill_id:
            raise ValueError("Required skill feature field 'skill_id' is missing.")

        # 2. Canonical ID format and validation warnings (Refinement 1)
        if not skill_id:
            msg = f"Skill entity '{entity.value}' has no canonical skill ID."
            self._logger.warning(
                "skill_validation_missing_canonical_id",
                extra={"entity_value": entity.value, "warning": msg},
            )
            warnings.append(msg)
        else:
            # Check prefix format if provided
            if not skill_id.startswith("SKL-"):
                msg = f"Skill ID '{skill_id}' does not conform to expected 'SKL-' prefix."
                self._logger.warning(
                    "skill_validation_invalid_id_prefix",
                    extra={"skill_id": skill_id, "warning": msg},
                )
                warnings.append(msg)

        # 3. Confidence range validation
        if entity.confidence < rules.confidence_threshold:
            raise ValueError(
                f"Skill confidence {entity.confidence} is below "
                f"configured threshold of {rules.confidence_threshold}."
            )

        # 4. Provenance check
        if not entity.location or not entity.location.segment_id:
            msg = f"Skill entity '{entity.value}' is missing complete physical provenance location."
            self._logger.warning(
                "skill_validation_missing_provenance",
                extra={"entity_value": entity.value, "warning": msg},
            )
            warnings.append(msg)

        return warnings
