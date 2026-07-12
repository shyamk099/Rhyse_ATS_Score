"""Pydantic schemas for structural analysis rule payloads.

Purpose:
    Provide strict validation for layout analyzer heuristics loaded via the Rule Engine.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class StructuralAnalysisRules(BaseModel):
    """Configuration heuristics governing physical layout block identification."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    max_heading_length: int = Field(default=80, ge=1)
    bullet_symbols: tuple[str, ...] = Field(default=("•", "-", "*", "▪", "◦", "▪"))
    numbered_patterns: tuple[str, ...] = Field(default=(r"^\d+[\.\)]\s+", r"^[a-zA-Z][\.\)]\s+"))
    heading_all_caps: bool = Field(default=True)
    table_min_delimiters: int = Field(default=2, ge=1)
    table_delimiters: tuple[str, ...] = Field(default=("|", "\t", "  "))
