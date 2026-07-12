"""Models representing education candidates, assembled records, and collections.

Purpose:
    Define immutable data schemas holding compound education fields,
    provenance references, and extraction statistics.
    Follows the standardized compound entity lifecycle:
    Candidate → Normalized → Assembled → Entity → Collection.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class EducationCandidate(BaseModel):
    """Intermediate candidate holding raw evidence matches from segment text."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    section_type: str = Field(min_length=1)
    raw_text: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    detected_dates: tuple[str, ...] = Field(default_factory=tuple)
    detected_institution: str | None = None
    detected_degree: str | None = None
    detected_major: str | None = None
    detected_gpa: str | None = None
    detected_grade: str | None = None
    has_graduation_indicator: bool = False


class NormalizedEducation(BaseModel):
    """Normalized intermediate education carrying cleaned field values."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    candidate: EducationCandidate
    institution_name: str | None = None
    degree: str | None = None
    specialization: str | None = None
    field_of_study: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    graduation_date_raw: str | None = None
    gpa_raw: str | None = None
    grade_raw: str | None = None


class AssembledEducation(BaseModel):
    """Compound education record grouping all evidence into one immutable aggregate."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    education_id: str = Field(min_length=1)
    institution_name: str | None = None
    degree: str | None = None
    specialization: str | None = None
    field_of_study: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    graduation_date_raw: str | None = None
    gpa_raw: str | None = None
    grade_raw: str | None = None
    honors: tuple[str, ...] = Field(default_factory=tuple)
    certifications: tuple[str, ...] = Field(default_factory=tuple)
    location_raw: str | None = None
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class EducationEntity(BaseModel):
    """Final immutable compound education entity with full provenance metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    education_id: str = Field(min_length=1)
    institution_name: str | None = None
    degree: str | None = None
    specialization: str | None = None
    field_of_study: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    graduation_date_raw: str | None = None
    gpa_raw: str | None = None
    grade_raw: str | None = None
    honors: tuple[str, ...] = Field(default_factory=tuple)
    certifications: tuple[str, ...] = Field(default_factory=tuple)
    location_raw: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = ""
    matched_rules: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class EducationExtractionStatistics(BaseModel):
    """Immutable execution statistics for education extraction runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_education_records: int = Field(ge=0)
    records_with_degree: int = Field(ge=0)
    records_with_gpa: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class EducationCollection(BaseModel):
    """Immutable aggregation contract containing all extracted education records."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[EducationEntity, ...]
    statistics: EducationExtractionStatistics
