"""Pydantic schemas representing configurable experience extraction rules.

Purpose:
    Define configuration schemas for date patterns, company indicators,
    role indicators, employment type mappings, and confidence thresholds
    loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class ExperienceExtractionRules(BaseModel):
    """Configuration heuristics governing deterministic experience parsing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    extraction_scope: Sequence[str] = Field(default=("EXPERIENCE",))

    date_patterns: Sequence[str] = Field(
        default=(
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
            r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
            r"Dec(?:ember)?)\s+\d{4}",
            r"\d{1,2}/\d{4}",
            r"\d{4}",
        )
    )

    current_employment_indicators: Sequence[str] = Field(
        default=("present", "current", "now", "ongoing", "till date"),
    )

    company_indicators: Sequence[str] = Field(
        default=(
            "Inc", "LLC", "Ltd", "Corp", "Corporation", "Company",
            "Group", "Technologies", "Solutions", "Consulting",
            "Services", "Systems", "Partners", "Associates",
            "Labs", "Studio", "Agency",
        ),
    )

    role_indicators: Sequence[str] = Field(
        default=(
            "Engineer", "Developer", "Architect", "Manager",
            "Director", "Lead", "Senior", "Junior", "Analyst",
            "Consultant", "Designer", "Administrator", "Specialist",
            "Coordinator", "Intern", "Associate", "Officer",
            "Head", "VP", "President", "Chief",
        ),
    )

    employment_type_mappings: Mapping[str, str] = Field(
        default={
            "full-time": "Full-Time",
            "full time": "Full-Time",
            "part-time": "Part-Time",
            "part time": "Part-Time",
            "contract": "Contract",
            "freelance": "Freelance",
            "internship": "Internship",
            "intern": "Internship",
            "temporary": "Temporary",
            "remote": "Remote",
        },
    )

    date_range_separator: str = Field(default=r"\s*[-–—to]+\s*")

    confidence_mappings: Mapping[str, float] = Field(
        default={
            "EXPERIENCE": 0.95,
            "DEFAULT": 0.6,
        }
    )

    default_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
