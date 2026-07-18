"""Pydantic configuration schema for Certification Matching Rules.

Purpose:
    Define configuration schemas loaded from the Rule Engine governing CertificationMatcher operations.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field


class CertificationMatchingRules(BaseModel):
    """Configuration heuristics governing comparison checks on Certification features."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalization: bool = Field(default=True)
    comparison_mode: str = Field(default="ALL")  # CANONICAL, NAME_ORG, NAME, ALL
    deterministic_ordering: bool = Field(default=True)
    logging_options: Mapping[str, Any] = Field(default_factory=dict)
