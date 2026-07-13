"""Pydantic schemas representing configurable skill feature extraction rules.

Purpose:
    Define configuration schemas for skill feature enablement, validation requirements,
    and normalization behaviors loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class SkillFeatureRules(BaseModel):
    """Configuration heuristics governing skill feature transformation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = Field(default=True)
    normalize_whitespace: bool = Field(default=True)
    required_fields: Sequence[str] = Field(default=("value",))
    confidence_threshold: float = Field(default=0.0, ge=0.0, le=1.0)
