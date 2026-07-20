"""Explainability Models.

Purpose:
    Define immutable Pydantic models (DTOs) for SectionExplanation,
    OverallExplanation, and ExplainabilityResult.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult


class SectionExplanation(BaseModel):
    """Immutable section explanation DTO holding formula, details and summary."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    section_name: str
    raw_score: float
    maximum_score: float
    normalized_score: float
    weight_used: float
    matched_items: tuple[str, ...] = Field(default_factory=tuple)
    missing_items: tuple[str, ...] = Field(default_factory=tuple)
    classification_counts: dict[str, int] = Field(default_factory=dict)
    formula: str
    summary: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class OverallExplanation(BaseModel):
    """Immutable overall score explanation DTO."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    overall_score: float
    formula: str
    section_contributions: dict[str, float] = Field(default_factory=dict)
    weight_configuration_version: str
    summary: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExplainabilityResult(BaseModel):
    """Immutable wrapper wrapping ScoreResult and its explanations."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    score_result: ScoreResult
    overall_explanation: OverallExplanation | None = None
    section_explanations: dict[str, SectionExplanation] = Field(default_factory=dict)
    statistics: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
