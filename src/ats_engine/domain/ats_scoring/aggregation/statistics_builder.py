"""AggregationStatisticsBuilder definition.

Purpose:
    Compile aggregation-level execution statistics as a plain immutable dict.
"""

from __future__ import annotations

from typing import Any


class AggregationStatisticsBuilder:
    """Builder producing aggregation execution telemetry as a plain dict[str, Any].

    Captures wall-clock timing split by normalization and weighting phases,
    alongside the computed overall score and versioning metadata.
    """

    @staticmethod
    def build(
        aggregation_time_ms: float = 0.0,
        normalization_time_ms: float = 0.0,
        weighting_time_ms: float = 0.0,
        overall_score: float | None = None,
        pipeline_version: str = "1.0.0",
        aggregation_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """Compile an immutable aggregation statistics record.

        Args:
            aggregation_time_ms: Total wall-clock time for the aggregate() call in ms.
            normalization_time_ms: Time spent normalizing all five sections in ms.
            weighting_time_ms: Time spent applying weights and computing overall in ms.
            overall_score: The computed overall ATS score, or None on failure.
            pipeline_version: Version string of the scoring pipeline.
            aggregation_version: Version of the aggregation engine.

        Returns:
            A plain dict[str, Any] with aggregation telemetry.
        """
        return {
            "aggregation_time_ms": round(aggregation_time_ms, 4),
            "normalization_time_ms": round(normalization_time_ms, 4),
            "weighting_time_ms": round(weighting_time_ms, 4),
            "overall_score": overall_score,
            "pipeline_version": pipeline_version,
            "aggregation_version": aggregation_version,
        }
