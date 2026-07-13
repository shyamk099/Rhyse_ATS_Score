"""Validation summary builder for feature audits.

Purpose:
    Compile validation errors, warnings, deduplication counts,
    and active rules versions into an audit summary.
"""

from __future__ import annotations

import datetime
from typing import Sequence

from ats_engine.domain.feature_engineering.models import (
    ValidationErrorDetail,
    ValidationSummary,
    ValidationWarningDetail,
)


class ValidationSummaryBuilder:
    """Builder assembling audit statistics into a ValidationSummary DTO."""

    @classmethod
    def build(
        cls,
        errors: Sequence[ValidationErrorDetail],
        warnings: Sequence[ValidationWarningDetail],
        duplicate_count: int,
        rules_version: str,
    ) -> ValidationSummary:
        """Create the ValidationSummary audit payload.

        Args:
            errors: Sequence of ValidationErrorDetail instances.
            warnings: Sequence of ValidationWarningDetail instances.
            duplicate_count: resolved duplicate counts.
            rules_version: active validation rule schema version.

        Returns:
            The immutable ValidationSummary object.
        """
        if errors:
            status = "INVALID"
        elif warnings:
            status = "WARNING"
        else:
            status = "VALID"

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

        return ValidationSummary(
            status=status,
            errors=tuple(errors),
            warnings=tuple(warnings),
            duplicate_count=duplicate_count,
            validation_timestamp=now_utc,
            rules_version=rules_version,
        )
