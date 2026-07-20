"""ScoreResult model definition.

Purpose:
    Define main ScoreResult container DTO.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata


class ScoreResult(BaseModel):
    """Immutable final ScoreResult DTO. Holds section scores, statistics, and validation details."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    overall_score: float | None = None
    skill_score: SectionScore | None = None
    experience_score: SectionScore | None = None
    education_score: SectionScore | None = None
    project_score: SectionScore | None = None
    certification_score: SectionScore | None = None
    statistics: ScoreStatistics
    metadata: ScoreMetadata
    warnings: tuple[str, ...] = Field(default_factory=tuple)
    validation_summary: dict[str, Any] = Field(default_factory=dict)
