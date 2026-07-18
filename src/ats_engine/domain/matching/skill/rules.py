"""Pydantic configuration schema for Skill Matching Rules.

Purpose:
    Define configuration schemas loaded from the Rule Engine governing SkillMatcher operations.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field


class SkillMatchingRules(BaseModel):
    """Configuration heuristics governing comparison checks on Skill features."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalization: bool = Field(default=True)
    comparison_mode: str = Field(default="CANONICAL")  # CANONICAL, ALL
    deterministic_ordering: bool = Field(default=True)
    logging_options: Mapping[str, Any] = Field(default_factory=dict)
