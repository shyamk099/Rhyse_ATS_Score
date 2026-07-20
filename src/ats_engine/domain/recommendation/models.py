"""Recommendation Models.

Purpose:
    Define immutable Pydantic models for Recommendation and RecommendationResult.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult


class RecommendationContext(BaseModel):
    """Immutable context wrapping upstream match, scoring, and explainability DTOs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    match_collection: CanonicalMatchCollection | None = None
    score_result: ScoreResult | None = None
    explainability_result: ExplainabilityResult | None = None
    custom_options: dict[str, Any] = Field(default_factory=dict)


class Recommendation(BaseModel):
    """Immutable recommendation DTO produced by a RecommendationProvider."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    recommendation_id: str = Field(min_length=1)
    section: str = Field(min_length=1)
    category: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    priority: int = Field(default=0, ge=0)
    impact: float = Field(default=0.0, ge=0.0, le=100.0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RecommendationResult(BaseModel):
    """Immutable result wrapper returned by RecommendationEngine.recommend()."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    context: RecommendationContext
    recommendations: tuple[Recommendation, ...] = Field(default_factory=tuple)
    statistics: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

