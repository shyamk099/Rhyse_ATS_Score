"""Pydantic schemas representing configurable canonical feature validation rules.

Purpose:
    Define configuration schemas for duplicate resolver policies, validation options,
    and threshold requirements loaded from the Rule Engine.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CanonicalFeatureValidationRules(BaseModel):
    """Configuration governing validation and duplicate resolution across the canonical collection."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    duplicate_policy: str = Field(default="KEEP_FIRST")  # KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL
    enable_cross_validation: bool = Field(default=True)
    rules_version: str = Field(default="canonical_rules_v1.0")
    confidence_threshold: float = Field(default=0.0, ge=0.0, le=1.0)
