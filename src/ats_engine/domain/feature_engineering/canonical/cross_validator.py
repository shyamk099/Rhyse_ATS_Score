"""Cross-collection relational validator.

Purpose:
    Verify references, ID duplication across domains, categories, and
    provenance consistency in a read-only manner.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ats_engine.domain.feature_engineering.models import (
    Feature,
    FeatureCategory,
    ValidationErrorDetail,
    ValidationWarningDetail,
)
from ats_engine.domain.feature_engineering.canonical.rules import CanonicalFeatureValidationRules
from ats_engine.infrastructure.logging.factory import LoggerFactory


class CrossFeatureValidator:
    """Relational validator verifying integrity across all feature collections."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize validator with optional logger dependency."""
        self._logger = logger or LoggerFactory.get_logger(__name__)

    def validate(
        self,
        features: Sequence[Feature],
        rules: CanonicalFeatureValidationRules,
    ) -> tuple[list[ValidationErrorDetail], list[ValidationWarningDetail]]:
        """Validate references and overlaps across all categories.

        Args:
            features: Consolidated sequence of Feature objects.
            rules: Active CanonicalFeatureValidationRules.

        Returns:
            A tuple of (errors_list, warnings_list).
        """
        errors: list[ValidationErrorDetail] = []
        warnings: list[ValidationWarningDetail] = []

        if not rules.enable_cross_validation:
            return errors, warnings

        id_counts: dict[str, int] = {}
        for feature in features:
            if feature.feature_id:
                id_counts[feature.feature_id] = id_counts.get(feature.feature_id, 0) + 1

        for feature in features:
            fid = feature.feature_id
            if not fid:
                continue

            # 1. Duplicated ID check across categories
            if id_counts[fid] > 1:
                errors.append(
                    ValidationErrorDetail(
                        feature_id=fid,
                        field="feature_id",
                        message=f"Duplicated feature ID '{fid}' across collection segments.",
                        error_type="duplicated_id",
                    )
                )

            # 2. Category matching provenance source check
            category = feature.category
            provenance_type = feature.provenance.source_entity_type

            if category == FeatureCategory.SKILL and provenance_type != "SKILL":
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_type",
                        message=f"Category SKILL has provenance source entity type '{provenance_type}'.",
                        warning_type="mismatched_provenance_type",
                    )
                )
            elif category == FeatureCategory.EXPERIENCE and provenance_type != "EXPERIENCE":
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_type",
                        message=f"Category EXPERIENCE has provenance source entity type '{provenance_type}'.",
                        warning_type="mismatched_provenance_type",
                    )
                )
            elif category == FeatureCategory.EDUCATION and provenance_type != "EDUCATION":
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_type",
                        message=f"Category EDUCATION has provenance source entity type '{provenance_type}'.",
                        warning_type="mismatched_provenance_type",
                    )
                )
            elif category == FeatureCategory.PROJECT and provenance_type != "PROJECT":
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_type",
                        message=f"Category PROJECT has provenance source entity type '{provenance_type}'.",
                        warning_type="mismatched_provenance_type",
                    )
                )
            elif category == FeatureCategory.CERTIFICATION and provenance_type != "CERTIFICATION":
                warnings.append(
                    ValidationWarningDetail(
                        feature_id=fid,
                        field="provenance.source_entity_type",
                        message=f"Category CERTIFICATION has provenance source entity type '{provenance_type}'.",
                        warning_type="mismatched_provenance_type",
                    )
                )

        return errors, warnings
