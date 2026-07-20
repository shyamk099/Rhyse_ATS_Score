"""ProjectStatisticsBuilder definition.

Purpose:
    Provide telemetry statistics builder for ProjectScorer execution runs.
"""

from __future__ import annotations

from typing import Any


class ProjectStatisticsBuilder:
    """Builder generating stats dict metrics for Project Scorer execution."""

    @staticmethod
    def build(
        matched_items: int = 0,
        missing_items: int = 0,
        exact_matches: int = 0,
        similar_projects: int = 0,
        related_projects: int = 0,
        partial_matches: int = 0,
        processing_time_ms: float = 0.0,
    ) -> dict[str, Any]:
        """Compile a dictionary containing operational metrics of Project scoring."""
        return {
            "matched_items": matched_items,
            "missing_items": missing_items,
            "exact_matches": exact_matches,
            "similar_projects": similar_projects,
            "related_projects": related_projects,
            "partial_matches": partial_matches,
            "processing_time_ms": processing_time_ms,
        }

