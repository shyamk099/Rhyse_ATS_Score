"""Pydantic configuration schema for Project Matching Rules.

Purpose:
    Define configuration schemas loaded from the Rule Engine governing ProjectMatcher operations.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field


class ProjectMatchingRules(BaseModel):
    """Configuration heuristics governing comparison checks on Project features."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalization: bool = Field(default=True)
    comparison_mode: str = Field(default="ALL")  # CANONICAL, NAME_ORG_ROLE, NAME_ROLE, NAME, ALL
    deterministic_ordering: bool = Field(default=True)
    logging_options: Mapping[str, Any] = Field(default_factory=dict)
