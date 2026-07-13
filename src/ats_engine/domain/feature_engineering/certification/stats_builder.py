"""Statistics logger helper for Certification feature engineering.

Purpose:
    Aggregate input/output metrics, count active status indicators,
    and log telemetry stats for diagnostics.
"""

from __future__ import annotations

from typing import Any


class CertificationFeatureStatisticsBuilder:
    """Stateless tracker for certification feature extraction metrics."""

    @classmethod
    def calculate(
        cls,
        input_count: int,
        output_count: int,
        warnings_count: int,
        active_count: int,
    ) -> dict[str, Any]:
        """Aggregate stats parameters into a single telemetry mapping.

        Args:
            input_count: Count of input extracted entities.
            output_count: Count of final unique Feature DTOs generated.
            warnings_count: Count of warnings during validation.
            active_count: Count of certification records with active status indicators.

        Returns:
            A metadata dictionary containing structural metrics.
        """
        return {
            "total_input_certification_records": input_count,
            "aggregated_features_count": output_count,
            "validation_warnings_count": warnings_count,
            "active_records_count": active_count,
        }
