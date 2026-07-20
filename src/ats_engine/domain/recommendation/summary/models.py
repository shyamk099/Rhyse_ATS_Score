"""Resume Intelligence Summary Models.

Purpose:
    Define immutable Pydantic DTO models for the Resume Intelligence Summary,
    including ResumeHealth, ResumeSectionSummary, ResumeIntelligenceStatistics,
    and the final ResumeIntelligenceSummary.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from ats_engine.domain.recommendation.models import Recommendation


class ResumeSectionSummary(BaseModel):
    """Immutable DTO summarizing recommendation counts for a single resume section."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    section: str = Field(min_length=1)
    total_recommendations: int = Field(ge=0)
    high_priority: int = Field(ge=0)
    medium_priority: int = Field(ge=0)
    low_priority: int = Field(ge=0)


class ResumeHealth(BaseModel):
    """Immutable DTO representing deterministic resume health status."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    score: float = Field(ge=0.0, le=100.0)
    grade: str = Field(min_length=1)
    status: str = Field(min_length=1)


class ResumeIntelligenceStatistics(BaseModel):
    """Immutable DTO holding metrics compiled by the summary engine."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    execution_time_ms: float = Field(ge=0.0)
    sections_processed: int = Field(ge=0)
    recommendations_processed: int = Field(ge=0)
    summary_generated: bool = True


class ResumeIntelligenceSummary(BaseModel):
    """Immutable DTO representing the final Resume Intelligence Summary — Book 07 output."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    overall_health: ResumeHealth
    total_recommendations: int = Field(ge=0)
    high_priority: int = Field(ge=0)
    medium_priority: int = Field(ge=0)
    low_priority: int = Field(ge=0)
    section_summaries: tuple[ResumeSectionSummary, ...] = Field(default_factory=tuple)
    top_recommendations: tuple[Recommendation, ...] = Field(default_factory=tuple)
    statistics: ResumeIntelligenceStatistics
    generated_at: datetime = Field(default_factory=datetime.utcnow)
