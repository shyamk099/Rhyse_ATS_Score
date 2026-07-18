"""Immutable domain models for ATS Matching Engine.

Purpose:
    Define pure, frozen Pydantic schemas representing matching outputs,
    statistics, metadata, locations, context, and collections.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence, Literal, Tuple
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.feature_engineering.models import (
    CanonicalFeatureCollection,
    FeatureLocation,
    FeatureProvenance,
)


class MatchLocation(BaseModel):
    """Immutable coordinates tracking matching points inside resume and job documents."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    resume_feature_location: FeatureLocation | None = None
    job_feature_location: FeatureLocation | None = None
    resume_page: int | None = Field(default=None, ge=1)
    job_page: int | None = Field(default=None, ge=1)
    resume_source_ids: tuple[str, ...] = Field(default_factory=tuple)
    job_source_ids: tuple[str, ...] = Field(default_factory=tuple)


class MatchMetadata(BaseModel):
    """Immutable metadata logs generated during matcher comparison runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    correlation_id: str = Field(min_length=1)
    matcher_type: str = Field(min_length=1)
    execution_timestamp: str = Field(min_length=1)
    rules_version: str = Field(min_length=1)
    custom_attributes: Mapping[str, Any] = Field(default_factory=dict)


class MatchResult(BaseModel):
    """Immutable result of comparing one resume feature against one job description feature."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    match_id: str = Field(min_length=1)
    matcher_type: str = Field(min_length=1)
    resume_feature_id: str = Field(min_length=1)
    job_feature_id: str = Field(min_length=1)
    metadata: MatchMetadata
    provenance: FeatureProvenance | None = None
    locations: MatchLocation | None = None


class MatchingStatistics(BaseModel):
    """Immutable execution performance and structural metrics logs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_resume_features: int = Field(default=0, ge=0)
    total_job_features: int = Field(default=0, ge=0)
    processed_features: int = Field(default=0, ge=0)
    processed_matchers: int = Field(default=0, ge=0)
    match_result_count: int = Field(default=0, ge=0)
    execution_duration_ms: float = Field(default=0.0, ge=0.0)


class MatchingContext(BaseModel):
    """Execution context variables passed across matching pipeline."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    resume_features: CanonicalFeatureCollection
    job_features: CanonicalFeatureCollection
    rule_payload: Mapping[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(min_length=1)
    execution_metadata: Mapping[str, Any] = Field(default_factory=dict)


class MatchCollection(BaseModel):
    """Official aggregate output DTO of Book 05."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    results: tuple[MatchResult, ...] = Field(default_factory=tuple)
    statistics: MatchingStatistics
    context: MatchingContext | None = None

class ValidationErrorDetail(BaseModel):
    """Immutable detail about a validation error detected in a MatchResult."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    match_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    field: str | None = None
    severity: Literal["error"] = "error"

class ValidationWarningDetail(BaseModel):
    """Immutable detail about a non‑critical validation warning."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    match_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    field: str | None = None
    severity: Literal["warning"] = "warning"

class ValidationSummary(BaseModel):
    """Aggregated validation outcomes for a canonical match collection build."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    errors: Tuple[ValidationErrorDetail, ...] = Field(default_factory=tuple)
    warnings: Tuple[ValidationWarningDetail, ...] = Field(default_factory=tuple)
    total_errors: int = Field(default=0, ge=0)
    total_warnings: int = Field(default=0, ge=0)

class MatchStatistics(BaseModel):
    """Structural statistics for canonical match collection execution."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_resume_features: int = Field(default=0, ge=0)
    total_job_features: int = Field(default=0, ge=0)
    total_matches: int = Field(default=0, ge=0)
    duplicate_count: int = Field(default=0, ge=0)
    validation_error_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    category_counts: Mapping[str, int] = Field(default_factory=dict)
    execution_duration_ms: float = Field(default=0.0, ge=0.0)

class CanonicalMatchCollection(BaseModel):
    """Immutable aggregate DTO exposing all matches and telemetry for downstream engines."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    results: Tuple[Any, ...] = Field(default_factory=tuple)  # Generic to avoid circular import
    statistics: MatchStatistics
    validation_summary: ValidationSummary
