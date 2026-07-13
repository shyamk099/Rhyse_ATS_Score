"""Pydantic schemas representing configurable validation and canonical collection rules.

Purpose:
    Define configuration schemas for duplicate resolution strategies,
    cross-reference validation behaviors, and structural validation thresholds.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class CanonicalValidationRules(BaseModel):
    """Configuration rules governing canonical validation and duplicate resolution."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    strict_cross_referencing: bool = Field(default=False)

    duplicate_strategy: str = Field(default="KEEP_HIGHEST_CONFIDENCE")

    merge_policy: str = Field(default="MERGE_NON_NULL")

    conflict_policy: str = Field(default="USE_FIRST")

    required_collections: Sequence[str] = Field(
        default=("contacts", "skills")
    )

    validate_url_formats: bool = Field(default=True)

    validate_provenance_offsets: bool = Field(default=True)
