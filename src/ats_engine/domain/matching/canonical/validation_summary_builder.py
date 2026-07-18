"""ValidationSummary builder for CanonicalMatchCollection.

Purpose:
    Compile validation errors and warning details into a unified summary model.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import (
    ValidationErrorDetail,
    ValidationWarningDetail,
    ValidationSummary,
)


class ValidationSummaryBuilder:
    """Builder compiling validation errors and warnings into an immutable summary."""

    @classmethod
    def build(
        cls,
        errors: Sequence[ValidationErrorDetail],
        warnings: Sequence[ValidationWarningDetail],
    ) -> ValidationSummary:
        """Construct the validation summary.

        Args:
            errors: Sequence of ValidationErrorDetail DTOs.
            warnings: Sequence of ValidationWarningDetail DTOs.

        Returns:
            An immutable ValidationSummary instance.
        """
        return ValidationSummary(
            errors=tuple(errors),
            warnings=tuple(warnings),
            total_errors=len(errors),
            total_warnings=len(warnings),
        )
