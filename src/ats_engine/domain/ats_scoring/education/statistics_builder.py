"""EducationStatisticsBuilder definition.

Purpose:
    Provide telemetry statistics builder for EducationScorer execution runs.
"""

from __future__ import annotations

from typing import Any


class EducationStatisticsBuilder:
    """Builder generating stats dict metrics for Education Scorer execution."""

    @staticmethod
    def build(
        matched_items: int = 0,
        missing_items: int = 0,
        exact_matches: int = 0,
        higher_than_required: int = 0,
        related_field: int = 0,
        lower_than_required: int = 0,
        unrelated_field: int = 0,
        processing_time_ms: float = 0.0,
    ) -> dict[str, Any]:
        """Compile a dictionary containing operational metrics of Education scoring."""
        return {
            "matched_items": matched_items,
            "missing_items": missing_items,
            "exact_matches": exact_matches,
            "higher_than_required": higher_than_required,
            "related_field": related_field,
            "lower_than_required": lower_than_required,
            "unrelated_field": unrelated_field,
            "processing_time_ms": processing_time_ms,
        }

