"""ScoreStatistics model definition.

Purpose:
    Define score execution statistics telemetry DTO.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScoreStatistics(BaseModel):
    """Immutable scoring execution metrics and telemetry DTO."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    total_sections: int = 0
    registered_scorers: tuple[str, ...] = Field(default_factory=tuple)
    executed_scorers: tuple[str, ...] = Field(default_factory=tuple)
    skipped_scorers: tuple[str, ...] = Field(default_factory=tuple)
    failed_scorers: tuple[str, ...] = Field(default_factory=tuple)
    warnings: tuple[str, ...] = Field(default_factory=tuple)
    validation_errors: tuple[str, ...] = Field(default_factory=tuple)
    processing_time_ms: float = 0.0
