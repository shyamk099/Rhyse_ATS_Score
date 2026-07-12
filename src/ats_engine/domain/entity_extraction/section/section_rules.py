"""Pydantic schema representing configurable section detection rules.

Purpose:
    Define configuration schemas for section aliases and confidence ratings
    loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class SectionDetectionRules(BaseModel):
    """Configuration heuristics governing physical block section parsing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    section_aliases: Mapping[str, Sequence[str]] = Field(
        default={
            "SUMMARY": ("summary", "professional summary", "about me", "objective"),
            "EXPERIENCE": ("experience", "work history", "employment", "professional experience"),
            "EDUCATION": ("education", "academic background", "studies", "degrees"),
            "SKILLS": ("skills", "technical skills", "technologies", "core competencies"),
            "PROJECTS": ("projects", "personal projects", "academic projects"),
            "CERTIFICATIONS": ("certifications", "licenses", "courses"),
            "AWARDS": ("awards", "honors", "achievements"),
            "PUBLICATIONS": ("publications", "articles", "papers"),
            "LANGUAGES": ("languages", "spoken languages"),
            "INTERESTS": ("interests", "hobbies"),
            "REFERENCES": ("references", "referees"),
        }
    )

    heading_confidence_default: float = Field(default=0.7, ge=0.0, le=1.0)
    heading_confidence_alias_match: float = Field(default=0.95, ge=0.0, le=1.0)
    max_heading_words: int = Field(default=6, ge=1)
