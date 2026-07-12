"""Rules definition schema for canonical document validation thresholds.

Purpose:
    Provide strict validation of validation thresholds loaded via the Rule Engine.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CanonicalValidationRules(BaseModel):
    """Configuration rules governing document integrity and consistency validation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    min_allowed_characters: int = Field(default=10, ge=0)
    max_allowed_pages: int = Field(default=50, ge=1)
    allowable_character_count_variance: float = Field(default=0.0, ge=0.0)
    enable_variance_tolerance: bool = Field(default=False)
