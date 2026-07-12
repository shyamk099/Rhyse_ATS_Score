"""Pydantic schemas representing configurable education extraction rules.

Purpose:
    Define configuration schemas for degree indicators, institution indicators,
    major/specialization indicators, GPA patterns, grade patterns,
    date patterns, and confidence thresholds loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class EducationExtractionRules(BaseModel):
    """Configuration heuristics governing deterministic education parsing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    extraction_scope: Sequence[str] = Field(default=("EDUCATION",))

    date_patterns: Sequence[str] = Field(
        default=(
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
            r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
            r"Dec(?:ember)?)\s+\d{4}",
            r"\d{1,2}/\d{4}",
            r"\d{4}",
        )
    )

    graduation_indicators: Sequence[str] = Field(
        default=("graduated", "graduation", "conferred", "awarded", "completed"),
    )

    institution_indicators: Sequence[str] = Field(
        default=(
            "University", "Institute", "College", "School",
            "Academy", "Polytechnic", "Conservatory",
            "Seminary", "Faculty",
        ),
    )

    degree_indicators: Sequence[str] = Field(
        default=(
            "Bachelor", "Master", "Doctor", "PhD", "Ph.D",
            "MBA", "B.S", "B.A", "M.S", "M.A", "B.E", "M.E",
            "B.Tech", "M.Tech", "B.Sc", "M.Sc", "B.Com", "M.Com",
            "BBA", "MCA", "BCA", "LLB", "LLM", "MD", "DDS",
            "Associate", "Diploma", "Certificate",
            "BSc", "MSc", "BCom", "MCom",
        ),
    )

    major_indicators: Sequence[str] = Field(
        default=(
            "in", "of", "specialization", "major", "concentration",
            "focus", "stream", "branch", "discipline",
        ),
    )

    gpa_patterns: Sequence[str] = Field(
        default=(
            r"(?:GPA|CGPA|CPI|SPI)\s*[:\-]?\s*(\d+\.?\d*)\s*/?\s*(\d+\.?\d*)?",
            r"(\d+\.?\d*)\s*/\s*(\d+\.?\d*)\s*(?:GPA|CGPA|CPI|SPI)",
        ),
    )

    grade_patterns: Sequence[str] = Field(
        default=(
            r"(?:Grade|Class|Division)\s*[:\-]?\s*(First|Second|Third|Distinction|"
            r"Summa Cum Laude|Magna Cum Laude|Cum Laude|Pass|Merit|"
            r"[A-F][+-]?)",
        ),
    )

    honors_indicators: Sequence[str] = Field(
        default=(
            "Summa Cum Laude", "Magna Cum Laude", "Cum Laude",
            "Honors", "Honours", "Distinction", "Dean's List",
            "Gold Medal", "Silver Medal", "Valedictorian",
            "Salutatorian", "With Distinction", "First Class",
        ),
    )

    confidence_mappings: Mapping[str, float] = Field(
        default={
            "EDUCATION": 0.95,
            "DEFAULT": 0.6,
        }
    )

    default_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
