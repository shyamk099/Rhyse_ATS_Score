"""ScoringRules model configuration.

Purpose:
    Define frozen, immutable configuration model for governing scoring pipeline executions.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScoringRules(BaseModel):
    """Immutable rules structure governing score normalization, weights, and strictness."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    normalization_enabled: bool = Field(default=False)
    penalty_enabled: bool = Field(default=False)
    bonus_enabled: bool = Field(default=False)
    weight_profile: str = Field(default="DEFAULT", min_length=1)
