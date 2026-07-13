"""Validation engine for Certification features.

Purpose:
    Ensure certification entity integrity, validate identifiers,
    and report warnings for missing fields or thresholds.
"""

from __future__ import annotations

import logging

from ats_engine.domain.entity_extraction.certification.certification_models import CertificationEntity
from ats_engine.domain.feature_engineering.common.validation import (
    validate_confidence_threshold,
    validate_required_fields,
)
from ats_engine.domain.feature_engineering.certification.rules import CertificationFeatureRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CertificationFeatureValidator:
    """Validator enforcing integrity checks and emitting warnings for raw/non-canonical data."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(self, entity: CertificationEntity, rules: CertificationFeatureRules) -> list[str]:
        """Perform checks on a Certification entity.

        Args:
            entity: The CertificationEntity being evaluated.
            rules: Active CertificationFeatureRules payload.

        Returns:
            A list of warning messages generated during validation.

        Raises:
            ValueError: If a required field is missing or validation fails strictly.
        """
        warnings: list[str] = []

        # 1. Required fields check
        metadata_map = {
            "issuing_organization": entity.issuing_organization,
            "credential_id": entity.credential_id_raw,
            "credential_url": entity.credential_url,
            "issue_date_raw": entity.issue_date_raw,
            "expiration_date_raw": entity.expiration_date_raw,
            "validity_status_raw": entity.validity_status_raw,
            "description": entity.description_raw,
        }
        validate_required_fields(
            entity_val=entity.certification_name,
            entity_metadata=metadata_map,
            required=rules.required_fields,
            field_mappings={"certification_name": "name"},
        )

        # 2. Canonical ID format and validation warnings
        certification_id = entity.certification_id
        if not certification_id:
            msg = "Certification entity has no certification ID."
            self._logger.warning(
                "certification_validation_missing_id",
                extra={"certification_name": entity.certification_name, "warning": msg},
            )
            warnings.append(msg)
        elif not certification_id.startswith("CERT-"):
            msg = f"Certification ID '{certification_id}' does not conform to expected 'CERT-' prefix."
            self._logger.warning(
                "certification_validation_invalid_id_prefix",
                extra={"certification_id": certification_id, "warning": msg},
            )
            warnings.append(msg)

        # 3. Confidence range validation
        validate_confidence_threshold(entity.confidence, rules.confidence_threshold)

        # 4. Provenance check
        if not entity.source_segment_ids:
            msg = f"Certification entity '{certification_id}' is missing physical provenance segment IDs."
            self._logger.warning(
                "certification_validation_missing_provenance",
                extra={"certification_id": certification_id, "warning": msg},
            )
            warnings.append(msg)

        return warnings
