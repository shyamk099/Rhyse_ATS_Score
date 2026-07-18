"""Pydantic configuration schema for Experience Matching Rules.

Purpose:
    Define configuration schemas loaded from the Rule Engine governing ExperienceMatcher operations.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field


class ExperienceMatchingRules(BaseModel):
    """Configuration heuristics governing comparison checks on Experience features."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalization: bool = Field(default=True)
    comparison_mode: str = Field(default="CANONICAL")  # CANONICAL, COMPANY_TITLE, ALL
    deterministic_ordering: bool = Field(default=True)
    logging_options: Mapping[str, Any] = Field(default_factory=dict)
