"""Prioritization Models.

Purpose:
    Define immutable Pydantic DTO models for recommendation prioritization,
    including priority profiles, keys, stats, and prioritized result containers.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from ats_engine.domain.recommendation.models import Recommendation


class PriorityKey(BaseModel):
    """Immutable lookup key identifying a category and section mapping."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    section: str = Field(min_length=1)
    category: str = Field(min_length=1)


class PriorityProfile(BaseModel):
    """Immutable profile holding deterministic priority, impact, and confidence values."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    priority: int = Field(ge=0)
    impact: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)


class PrioritizationStatistics(BaseModel):
    """Immutable DTO holding metrics compiled by the prioritization engine."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    execution_time_ms: float = Field(ge=0.0)
    recommendations_processed: int = Field(ge=0)
    high_priority: int = Field(ge=0)
    medium_priority: int = Field(ge=0)
    low_priority: int = Field(ge=0)
    average_priority: float = Field(ge=0.0)
    average_impact: float = Field(ge=0.0, le=1.0)
    average_confidence: float = Field(ge=0.0, le=1.0)
    success: bool = True


class PrioritizedRecommendationResult(BaseModel):
    """Immutable result wrapper containing prioritized and sorted recommendations."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    recommendations: tuple[Recommendation, ...] = Field(default_factory=tuple)
    statistics: PrioritizationStatistics
    total_recommendations: int = Field(ge=0)
    high_priority: int = Field(ge=0)
    medium_priority: int = Field(ge=0)
    low_priority: int = Field(ge=0)
