"""ScoreMetadata model definition.

Purpose:
    Define score execution metadata containing engine versions and generation timestamp.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScoreMetadata(BaseModel):
    """Immutable scoring pipeline execution metadata DTO."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    engine_version: str
    rules_version: str
    generated_at: str
    processing_time_ms: float = 0.0
    pipeline_version: str
    book_version: str = Field(default="6")
    milestone: str = Field(default="6.1")
