"""RecommendationStatisticsBuilder definition.

Purpose:
    Compile recommendation execution statistics as a plain dict.
"""

from __future__ import annotations

from typing import Any


class RecommendationStatisticsBuilder:
    """Builder producing recommendation execution statistics."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        providers_executed: tuple[str, ...] = (),
        recommendations_generated: int = 0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary.

        Args:
            execution_time_ms: Total wall-clock time for the recommend() call.
            providers_executed: Tuple of provider names that were executed.
            recommendations_generated: Total number of recommendations produced.
            success: Whether the execution completed without error.

        Returns:
            A plain dict with execution telemetry.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "providers_executed": tuple(providers_executed),
            "recommendations_generated": recommendations_generated,
            "success": success,
        }
