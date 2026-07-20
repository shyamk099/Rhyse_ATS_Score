"""EducationScoringRules definition.

Purpose:
    Define immutable scoring parameters for concrete Education scoring.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EducationScoringRules(BaseModel):
    """Configuration structure controlling Education scoring weights and defaults."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    exact_match_weight: float = Field(default=4.0, ge=0.0)
    higher_than_required_weight: float = Field(default=4.0, ge=0.0)
    related_field_weight: float = Field(default=2.5, ge=0.0)
    lower_than_required_weight: float = Field(default=1.0, ge=0.0)
    unrelated_field_weight: float = Field(default=0.0, ge=0.0)
    maximum_education_score: float = Field(default=15.0, ge=0.0)
    minimum_education_score: float = Field(default=0.0, ge=0.0)
    allow_related_fields: bool = Field(default=True)

