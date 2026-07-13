"""Models representing project candidates, assembled records, and collections.

Purpose:
    Define immutable data schemas holding compound project fields,
    provenance references, and extraction statistics.
    Follows the standardized compound entity lifecycle:
    Candidate → Normalized → Assembled → Entity → Collection.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class ProjectTechnology(BaseModel):
    """Immutable representation of a technology integrating with canonical Skill IDs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    raw_name: str = Field(min_length=1)
    skill_id: str | None = None


class ProjectURL(BaseModel):
    """Immutable representation of a URL preserving provenance details."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    original_value: str = Field(min_length=1)
    normalized_value: str = Field(min_length=1)
    matched_rule: str = Field(min_length=1)


class ProjectCandidate(BaseModel):
    """Intermediate candidate holding raw evidence matches from segment text."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    section_type: str = Field(min_length=1)
    raw_text: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    detected_dates: tuple[str, ...] = Field(default_factory=tuple)
    detected_name: str | None = None
    detected_organization: str | None = None
    detected_role: str | None = None
    detected_repo_url: str | None = None
    detected_demo_url: str | None = None


class NormalizedProject(BaseModel):
    """Normalized intermediate project carrying cleaned field values."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    candidate: ProjectCandidate
    project_name: str | None = None
    organization: str | None = None
    role: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    duration_raw: str | None = None
    repo_url: ProjectURL | None = None
    demo_url: ProjectURL | None = None


class AssembledProject(BaseModel):
    """Compound project record grouping all evidence into one immutable aggregate."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    project_id: str = Field(min_length=1)
    project_name: str | None = None
    organization: str | None = None
    role: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    duration_raw: str | None = None
    technologies: tuple[ProjectTechnology, ...] = Field(default_factory=tuple)
    responsibilities: tuple[str, ...] = Field(default_factory=tuple)
    achievements: tuple[str, ...] = Field(default_factory=tuple)
    project_description: str | None = None
    repo_url: ProjectURL | None = None
    demo_url: ProjectURL | None = None
    location_raw: str | None = None
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class ProjectEntity(BaseModel):
    """Final immutable compound project entity with full provenance metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    project_id: str = Field(min_length=1)
    project_name: str | None = None
    organization: str | None = None
    role: str | None = None
    start_date_raw: str | None = None
    end_date_raw: str | None = None
    duration_raw: str | None = None
    technologies: tuple[ProjectTechnology, ...] = Field(default_factory=tuple)
    responsibilities: tuple[str, ...] = Field(default_factory=tuple)
    achievements: tuple[str, ...] = Field(default_factory=tuple)
    project_description: str | None = None
    repo_url: ProjectURL | None = None
    demo_url: ProjectURL | None = None
    location_raw: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = ""
    matched_rules: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class ProjectExtractionStatistics(BaseModel):
    """Immutable execution statistics for project extraction runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_projects: int = Field(ge=0)
    projects_with_repo: int = Field(ge=0)
    projects_with_demo: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class ProjectCollection(BaseModel):
    """Immutable aggregation contract containing all extracted project records."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[ProjectEntity, ...]
    statistics: ProjectExtractionStatistics
