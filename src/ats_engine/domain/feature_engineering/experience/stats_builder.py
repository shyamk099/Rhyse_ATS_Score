"""Statistics logger helper for Experience feature engineering.

Purpose:
    Aggregate input/output metrics, count current employments,
    and log telemetry stats for diagnostics.
"""

from __future__ import annotations

from typing import Any


class ExperienceFeatureStatisticsBuilder:
    """Stateless tracker for experience feature extraction metrics."""

    @classmethod
    def calculate(
        cls,
        input_count: int,
        output_count: int,
        warnings_count: int,
        current_count: int,
    ) -> dict[str, Any]:
        """Aggregate stats parameters into a single telemetry mapping.

        Args:
            input_count: Count of input extracted entities.
            output_count: Count of final unique Feature DTOs generated.
            warnings_count: Count of warnings during validation.
            current_count: Count of current employment records.

        Returns:
            A metadata dictionary containing structural metrics.
        """
        return {
            "total_input_experiences": input_count,
            "aggregated_features_count": output_count,
            "validation_warnings_count": warnings_count,
            "current_employments_count": current_count,
        }
