"""CertificationScoringRules definition.

Purpose:
    Define immutable scoring parameters for concrete Certification scoring.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CertificationScoringRules(BaseModel):
    """Configuration structure controlling Certification scoring weights and defaults."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    version: str = Field(default="1.0.0", min_length=1)
    strictness: str = Field(default="STRICT", min_length=1)
    exact_match_weight: float = Field(default=3.0, ge=0.0)
    equivalent_certification_weight: float = Field(default=2.5, ge=0.0)
    related_certification_weight: float = Field(default=2.0, ge=0.0)
    partial_match_weight: float = Field(default=1.0, ge=0.0)
    expired_certification_weight: float = Field(default=0.5, ge=0.0)
    maximum_certification_score: float = Field(default=10.0, ge=0.0)
    minimum_certification_score: float = Field(default=0.0, ge=0.0)
    allow_related_certifications: bool = Field(default=True)
    count_expired_certifications: bool = Field(default=True)
