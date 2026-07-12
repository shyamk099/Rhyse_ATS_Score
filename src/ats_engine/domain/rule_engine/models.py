"""Pydantic v2 models for rule engine envelopes.

Purpose:
    Define immutable representations of rules and their metadata envelopes.
"""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class RuleMetadata(BaseModel):
    """Metadata describing a single rule configuration."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    rule_id: str = Field(min_length=1)
    rule_version: str = Field(min_length=1)
    effective_date: str = Field(min_length=1)
    status: str = Field(min_length=1)
    description: str | None = None


class RuleEnvelope(BaseModel):
    """Generic envelope wrapping a rule configuration and its audit metadata."""

    model_config = ConfigDict(frozen=True, extra="ignore", str_strip_whitespace=True)

    metadata: RuleMetadata
    checksum: str = Field(min_length=1)
    source: str = Field(min_length=1)
    loaded_timestamp: str = Field(min_length=1)
    payload: dict[str, Any]
