"""Statistics logger helper for Project feature engineering.

Purpose:
    Aggregate input/output metrics, count records with technologies,
    and log telemetry stats for diagnostics.
"""

from __future__ import annotations

from typing import Any


class ProjectFeatureStatisticsBuilder:
    """Stateless tracker for project feature extraction metrics."""

    @classmethod
    def calculate(
        cls,
        input_count: int,
        output_count: int,
        warnings_count: int,
        tech_count: int,
    ) -> dict[str, Any]:
        """Aggregate stats parameters into a single telemetry mapping.

        Args:
            input_count: Count of input extracted entities.
            output_count: Count of final unique Feature DTOs generated.
            warnings_count: Count of warnings during validation.
            tech_count: Count of project records with technologies.

        Returns:
            A metadata dictionary containing structural metrics.
        """
        return {
            "total_input_project_records": input_count,
            "aggregated_features_count": output_count,
            "validation_warnings_count": warnings_count,
            "tech_records_count": tech_count,
        }
