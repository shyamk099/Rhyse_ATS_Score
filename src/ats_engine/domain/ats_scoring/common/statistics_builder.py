"""ScoreStatisticsBuilder definition.

Purpose:
    Expose telemetry compiling for scoring pipeline executions.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics


class ScoreStatisticsBuilder:
    """Builder generating immutable telemetry packages after score pipeline runs."""

    @staticmethod
    def build(
        total_sections: int = 0,
        registered_scorers: Sequence[str] = (),
        executed_scorers: Sequence[str] = (),
        skipped_scorers: Sequence[str] = (),
        failed_scorers: Sequence[str] = (),
        warnings: Sequence[str] = (),
        validation_errors: Sequence[str] = (),
        processing_time_ms: float = 0.0,
    ) -> ScoreStatistics:
        """Compile a frozen ScoreStatistics DTO containing operational telemetries."""
        return ScoreStatistics(
            total_sections=total_sections,
            registered_scorers=tuple(registered_scorers),
            executed_scorers=tuple(executed_scorers),
            skipped_scorers=tuple(skipped_scorers),
            failed_scorers=tuple(failed_scorers),
            warnings=tuple(warnings),
            validation_errors=tuple(validation_errors),
            processing_time_ms=processing_time_ms,
        )
