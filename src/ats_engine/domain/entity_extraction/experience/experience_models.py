"""Models representing experience candidates, assembled records, and collections.

Purpose:
    Define immutable data schemas holding compound experience fields,
    provenance references, and extraction statistics.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class ExperienceCandidate(BaseModel):
    """Intermediate candidate holding raw evidence matches from segment text."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    section_type: str = Field(min_length=1)
    raw_text: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    detected_dates: tuple[str, ...] = Field(default_factory=tuple)
    detected_company: str | None = None
    detected_title: str | None = None
    detected_employment_type: str | None = None
    is_current: bool = False


class NormalizedExperience(BaseModel):
    """Normalized intermediate experience carrying cleaned field values."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    candidate: ExperienceCandidate
    company_name: str | None = None
    job_title: str | None = None
    employment_type: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    is_current: bool = False


class AssembledExperience(BaseModel):
    """Compound experience record grouping all evidence into one immutable aggregate."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    experience_id: str = Field(min_length=1)
    company_name: str | None = None
    job_title: str | None = None
    employment_type: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    is_current: bool = False
    responsibilities: tuple[str, ...] = Field(default_factory=tuple)
    technologies: tuple[str, ...] = Field(default_factory=tuple)
    achievements: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class ExperienceEntity(BaseModel):
    """Final immutable compound experience entity with full provenance metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    experience_id: str = Field(min_length=1)
    company_name: str | None = None
    job_title: str | None = None
    employment_type: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    is_current: bool = False
    responsibilities: tuple[str, ...] = Field(default_factory=tuple)
    technologies: tuple[str, ...] = Field(default_factory=tuple)
    achievements: tuple[str, ...] = Field(default_factory=tuple)
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = ""
    matched_rules: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class ExperienceExtractionStatistics(BaseModel):
    """Immutable execution statistics for experience extraction runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_experiences: int = Field(ge=0)
    current_employment_count: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class ExperienceCollection(BaseModel):
    """Immutable aggregation contract containing all extracted experience records."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[ExperienceEntity, ...]
    statistics: ExperienceExtractionStatistics
