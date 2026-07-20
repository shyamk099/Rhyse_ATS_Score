"""ScoreBreakdown model definition.

Purpose:
    Define generic immutable ScoreBreakdown DTO carrying matching breakdown details.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class ScoreBreakdown(BaseModel):
    """Immutable scoring breakdown DTO holding itemized matching performance."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    matched_items: tuple[str, ...] = Field(default_factory=tuple)
    missing_items: tuple[str, ...] = Field(default_factory=tuple)
    classification_counts: dict[str, int] = Field(default_factory=dict)
    raw_points: float = Field(default=0.0, ge=0.0)
    maximum_points: float = Field(default=0.0, ge=0.0)
    rules_version: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)
