"""SkillStatisticsBuilder definition.

Purpose:
    Provide generic telemetry statistics builder for SkillScorer execution runs.
"""

from __future__ import annotations

from typing import Any


class SkillStatisticsBuilder:
    """Builder generating stats dict metrics for Skill Scorer execution."""

    @staticmethod
    def build(
        matched_items: int = 0,
        missing_items: int = 0,
        mandatory_matches: int = 0,
        optional_matches: int = 0,
        raw_points: float = 0.0,
        total_items: int = 0,
        processing_time_ms: float = 0.0,
    ) -> dict[str, Any]:
        """Compile a dictionary containing operational metrics of Skill scoring."""
        return {
            "matched_items": matched_items,
            "missing_items": missing_items,
            "mandatory_matches": mandatory_matches,
            "optional_matches": optional_matches,
            "raw_points": raw_points,
            "total_items": total_items,
            "processing_time_ms": processing_time_ms,
        }

