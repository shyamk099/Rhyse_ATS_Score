"""Statistics logger helper for Skill feature engineering.

Purpose:
    Aggregate input/output metrics, count unregistered raw skills,
    and log telemetry stats for diagnostics.
"""

from __future__ import annotations

from typing import Any


class SkillFeatureStatisticsBuilder:
    """Stateless tracker for skill feature extraction metrics."""

    @classmethod
    def calculate(
        cls,
        input_count: int,
        output_count: int,
        warnings_count: int,
        unregistered_count: int,
    ) -> dict[str, Any]:
        """Aggregate stats parameters into a single telemetry mapping.

        Args:
            input_count: Count of input extracted entities.
            output_count: Count of final unique Feature DTOs generated.
            warnings_count: Count of warnings during validation.
            unregistered_count: Count of skills missing canonical IDs.

        Returns:
            A metadata dictionary containing structural metrics.
        """
        return {
            "total_input_skills": input_count,
            "aggregated_features_count": output_count,
            "validation_warnings_count": warnings_count,
            "unregistered_raw_skills": unregistered_count,
        }
