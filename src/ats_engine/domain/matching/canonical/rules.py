"""Canonical matching configuration rules.

Defines immutable configuration for the canonical match collection pipeline.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CanonicalMatchingRules(BaseModel):
    """Immutable rule set governing canonical match collection processing."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    enabled: bool = Field(default=True)
    deterministic_ordering: bool = Field(default=True)
    duplicate_policy: Literal["KEEP_FIRST", "KEEP_LAST", "KEEP_HIGHEST_CONFIDENCE", "KEEP_ALL"] = Field(default="KEEP_FIRST")
    validation_mode: Literal["STRICT", "LENIENT"] = Field(default="STRICT")
    rules_version: str = Field(default="canonical_rules_v1.0")
