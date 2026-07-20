"""ExperienceScoringRules definition.

Purpose:
    Define immutable scoring parameters for concrete Experience scoring.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ExperienceScoringRules(BaseModel):
    """Configuration structure controlling Experience scoring weights and defaults."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    exact_match_weight: float = Field(default=3.0, ge=0.0)
    partial_match_weight: float = Field(default=1.5, ge=0.0)
    overqualified_weight: float = Field(default=3.0, ge=0.0)
    underqualified_weight: float = Field(default=0.5, ge=0.0)
    maximum_experience_score: float = Field(default=25.0, ge=0.0)
    minimum_experience_score: float = Field(default=0.0, ge=0.0)
    allow_partial_matching: bool = Field(default=True)
