"""SectionScore model definition.

Purpose:
    Define individual section score structure containing reference to ScoreBreakdown.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown


class SectionScore(BaseModel):
    """Immutable section score DTO referencing details breakdown."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    section_name: str
    raw_score: float | None = None
    normalized_score: float | None = None
    maximum_score: float | None = None
    weight: float | None = None
    breakdown: ScoreBreakdown | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

