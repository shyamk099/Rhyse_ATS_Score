"""Pydantic configuration schema for Education Matching Rules.

Purpose:
    Define configuration schemas loaded from the Rule Engine governing EducationMatcher operations.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field


class EducationMatchingRules(BaseModel):
    """Configuration heuristics governing comparison checks on Education features."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalization: bool = Field(default=True)
    comparison_mode: str = Field(default="ALL")  # CANONICAL, INSTITUTION_DEGREE, INSTITUTION_DEGREE_MAJOR, INSTITUTION_DEGREE_MAJOR_SPECIALIZATION, ALL
    deterministic_ordering: bool = Field(default=True)
    logging_options: Mapping[str, Any] = Field(default_factory=dict)
