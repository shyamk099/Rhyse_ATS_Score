"""SkillScoringRules definition.

Purpose:
    Define immutable scoring parameters for concrete Skill scoring.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SkillScoringRules(BaseModel):
    """Configuration structure controlling Skill scoring weights and defaults."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    mandatory_skill_weight: float = Field(default=2.0, ge=0.0)
    optional_skill_weight: float = Field(default=1.0, ge=0.0)
    maximum_skill_score: float = Field(default=40.0, ge=0.0)
    minimum_skill_score: float = Field(default=0.0, ge=0.0)
    allow_partial_matching: bool = Field(default=False)
