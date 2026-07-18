"""Pydantic schemas representing configurable matching rules.

Purpose:
    Define configuration schemas for matching engine enablement, matcher orders,
    logging flags, and timeouts.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class MatchingRules(BaseModel):
    """Configuration governing rule executions across the Matching Engine pipeline."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled_matchers: Sequence[str] = Field(default_factory=tuple)
    execution_order: Sequence[str] = Field(default_factory=tuple)
    enable_logging: bool = Field(default=True)
    timeout_seconds: float = Field(default=30.0, ge=0.0)
    rules_version: str = Field(default="matching_rules_v1.0")
