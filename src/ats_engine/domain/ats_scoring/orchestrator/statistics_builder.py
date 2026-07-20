"""OrchestratorStatisticsBuilder definition.

Purpose:
    Compile orchestration-level execution statistics capturing wall-clock
    timing, per-section timing, and execution outcome metadata.
"""

from __future__ import annotations

from typing import Any


class OrchestratorStatisticsBuilder:
    """Builder producing orchestration-level telemetry as a plain immutable dict.

    Orchestration statistics are distinct from pipeline statistics:
    - Pipeline stats: per-scorer result compilation.
    - Orchestrator stats: wall-clock coordination timing and lifecycle metadata.
    """

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        section_execution_times: dict[str, float] | None = None,
        sections_executed: tuple[str, ...] = (),
        sections_skipped: tuple[str, ...] = (),
        failed_sections: tuple[str, ...] = (),
        pipeline_version: str = "1.0.0",
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile an immutable orchestration statistics record.

        Args:
            execution_time_ms: Total wall-clock time for the orchestrate() call in ms.
            section_execution_times: Per-scorer name → elapsed ms mapping.
            sections_executed: Names of scorers that executed successfully.
            sections_skipped: Names of scorers that were disabled and skipped.
            failed_sections: Names of scorers that raised exceptions.
            pipeline_version: The pipeline version string from factory/metadata.
            success: True if orchestration completed without fatal failure.

        Returns:
            A plain dict[str, Any] with orchestration telemetry. Kept as a dict
            to avoid adding a new DTO to the models layer at this milestone.
        """
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "section_execution_times": dict(section_execution_times or {}),
            "sections_executed": tuple(sections_executed),
            "sections_skipped": tuple(sections_skipped),
            "failed_sections": tuple(failed_sections),
            "pipeline_version": pipeline_version,
            "success": success,
        }
