"""Orchestrated Recommendation Models.

Purpose:
    Define immutable Pydantic DTO models for recommendation orchestration,
    including OrchestratedRecommendationResult and OrchestrationStatistics.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field
from ats_engine.domain.recommendation.models import Recommendation


class OrchestrationStatistics(BaseModel):
    """Immutable DTO holding metrics compiled by the orchestration engine."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    execution_time_ms: float = Field(ge=0.0)
    recommendations_processed: int = Field(ge=0)
    sections: int = Field(ge=0)
    categories: int = Field(ge=0)
    high_priority: int = Field(ge=0)
    medium_priority: int = Field(ge=0)
    low_priority: int = Field(ge=0)
    largest_section: str
    largest_category: str
    success: bool = True


class OrchestratedRecommendationResult(BaseModel):
    """Immutable result wrapper containing fully grouped and indexed recommendations."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    recommendations: tuple[Recommendation, ...] = Field(default_factory=tuple)
    grouped_recommendations: Mapping[str, tuple[Recommendation, ...]] = Field(default_factory=dict)
    recommendations_by_section: Mapping[str, tuple[Recommendation, ...]] = Field(default_factory=dict)
    recommendations_by_priority: Mapping[str, tuple[Recommendation, ...]] = Field(default_factory=dict)
    statistics: OrchestrationStatistics
    total_recommendations: int = Field(ge=0)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
