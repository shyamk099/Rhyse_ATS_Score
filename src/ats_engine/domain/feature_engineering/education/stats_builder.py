"""Statistics logger helper for Education feature engineering.

Purpose:
    Aggregate input/output metrics, count records with degrees,
    and log telemetry stats for diagnostics.
"""

from __future__ import annotations

from typing import Any


class EducationFeatureStatisticsBuilder:
    """Stateless tracker for education feature extraction metrics."""

    @classmethod
    def calculate(
        cls,
        input_count: int,
        output_count: int,
        warnings_count: int,
        degree_count: int,
    ) -> dict[str, Any]:
        """Aggregate stats parameters into a single telemetry mapping.

        Args:
            input_count: Count of input extracted entities.
            output_count: Count of final unique Feature DTOs generated.
            warnings_count: Count of warnings during validation.
            degree_count: Count of education records with degrees.

        Returns:
            A metadata dictionary containing structural metrics.
        """
        return {
            "total_input_education_records": input_count,
            "aggregated_features_count": output_count,
            "validation_warnings_count": warnings_count,
            "degree_records_count": degree_count,
        }
