"""ExplainabilityStatisticsBuilder definition.

Purpose:
    Compile explainability execution statistics.
"""

from __future__ import annotations

from typing import Any


class ExplainabilityStatisticsBuilder:
    """Builder producing explainability execution statistics."""

    @staticmethod
    def build(
        execution_time_ms: float = 0.0,
        sections_processed: tuple[str, ...] = (),
        formula_generation_time_ms: float = 0.0,
        formatting_time_ms: float = 0.0,
        success: bool = True,
    ) -> dict[str, Any]:
        """Compile statistics dictionary."""
        return {
            "execution_time_ms": round(execution_time_ms, 4),
            "sections_processed": tuple(sections_processed),
            "formula_generation_time_ms": round(formula_generation_time_ms, 4),
            "formatting_time_ms": round(formatting_time_ms, 4),
            "success": success,
        }
