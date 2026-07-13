"""Read-only Feature validation engine.

Purpose:
    Perform structural checks, range evaluations, and field integrity reviews
    on individual Feature objects without modifying them.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.feature_engineering.models import (
    Feature,
    ValidationErrorDetail,
    ValidationWarningDetail,
)
from ats_engine.domain.feature_engineering.canonical.rules import CanonicalFeatureValidationRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class FeatureValidator:
    """Read-only validator performing structural checks on features."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(
        self,
        features: Sequence[Feature],
        rules: CanonicalFeatureValidationRules,
    ) -> tuple[list[ValidationErrorDetail], list[ValidationWarningDetail]]:
        """Validate list of features against configuration heuristics.

        Args:
            features: Sequence of Feature objects.
            rules: Active CanonicalFeatureValidationRules.

        Returns:
            A tuple containing (errors_list, warnings_list).
        """
        errors: list[ValidationErrorDetail] = []
        warnings: list[ValidationWarningDetail] = []

        for feature in features:
            fid = feature.feature_id

            # 1. Check feature ID
            if not fid or not fid.strip():
                errors.append(
                    ValidationErrorDetail(
                        feature_id=None,
                        field="feature_id",
                        message="Feature is missing feature_id.",
                        error_type="missing_field",
                    )
                )
                continue

            # 2. Check name
            if not feature.name or not feature.name.strip():
                errors.append(
                    ValidationErrorDetail(
                        feature_id=fid,
                        field="name",
                        message="Feature is missing name.",
                        error_type="missing_field",
                    )
                )

            # 3. Check confidence range
            if feature.confidence < 0.0 or feature.confidence > 1.0:
                errors.append(
                    ValidationErrorDetail(
                        feature_id=fid,
                        field="confidence",
                        message=f"Confidence {feature.confidence} is out of bounds [0.0, 1.0].",
                        error_type="out_of_bounds",
                    )
                )

            # 4. Check confidence threshold
            if feature.confidence < rules.confidence_threshold:
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="confidence",
                        message=f"Confidence {feature.confidence} is below threshold {rules.confidence_threshold}.",
                        warning_type="low_confidence",
                    )
                )

            # 5. Check provenance source entity ID
            if not feature.provenance or not feature.provenance.source_entity_id:
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_id",
                        message="Feature is missing source_entity_id in provenance.",
                        warning_type="missing_provenance_id",
                    )
                )

        return errors, warnings
