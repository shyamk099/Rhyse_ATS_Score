"""Pydantic schemas for document segmentation rule payloads.

Purpose:
    Provide strict validation of physical block grouping thresholds loaded via the Rule Engine.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SegmentationRules(BaseModel):
    """Configuration heuristics governing physical block grouping into segments."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    max_segment_characters: int = Field(default=1500, ge=100)
    max_segment_blocks: int = Field(default=8, ge=1)
    split_on_page_transition: bool = Field(default=True)
