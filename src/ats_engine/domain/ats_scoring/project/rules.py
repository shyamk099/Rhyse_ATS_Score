"""ProjectScoringRules definition.

Purpose:
    Define immutable scoring parameters for concrete Project scoring.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProjectScoringRules(BaseModel):
    """Configuration structure controlling Project scoring weights and defaults."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    exact_match_weight: float = Field(default=3.0, ge=0.0)
    similar_project_weight: float = Field(default=2.5, ge=0.0)
    related_project_weight: float = Field(default=2.0, ge=0.0)
    partial_match_weight: float = Field(default=1.0, ge=0.0)
    maximum_project_score: float = Field(default=15.0, ge=0.0)
    minimum_project_score: float = Field(default=0.0, ge=0.0)
    allow_related_projects: bool = Field(default=True)
