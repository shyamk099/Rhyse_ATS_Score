"""Immutable domain models for Feature Engineering.

Purpose:
    Define pure, frozen Pydantic schemas representing extracted features,
    locations, provenance metadata, execution context, and stats.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class FeatureCategory(str, Enum):
    """Enumeration of generic feature categories in Book 04."""

    SKILL = "SKILL"
    EXPERIENCE = "EXPERIENCE"
    EDUCATION = "EDUCATION"
    PROJECT = "PROJECT"
    CERTIFICATION = "CERTIFICATION"


class FeatureLocation(BaseModel):
    """Immutable coordinates indicating origin within source raw/layout documents."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    page_number: int | None = Field(default=None, ge=1)
    block_index: int | None = Field(default=None, ge=0)
    line_index: int | None = Field(default=None, ge=0)
    start_character: int | None = Field(default=None, ge=0)
    end_character: int | None = Field(default=None, ge=0)


class FeatureProvenance(BaseModel):
    """Immutable metadata tracking source entity and rule provenance."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    source_entity_id: str | None = None
    source_entity_type: str | None = None
    source_section: str | None = None
    source_document: str | None = None
    matched_rules: tuple[str, ...] = Field(default_factory=tuple)


class FeatureMetadata(BaseModel):
    """Immutable dictionary wrapper containing tracking attributes."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    creation_timestamp: str = Field(min_length=1)
    extractor_name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    custom_attributes: Mapping[str, Any] = Field(default_factory=dict)


class Feature(BaseModel):
    """Generic immutable feature object representation."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    feature_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: FeatureCategory
    value: Any
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    locations: tuple[FeatureLocation, ...] = Field(default_factory=tuple)
    provenance: FeatureProvenance
    metadata: FeatureMetadata


class FeatureEngineeringStatistics(BaseModel):
    """Immutable performance and structural metric logs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_features_extracted: int = Field(default=0, ge=0)
    extractor_counts: Mapping[str, int] = Field(default_factory=dict)
    execution_duration_seconds: float = Field(default=0.0, ge=0.0)


class FeatureExtractionContext(BaseModel):
    """Execution payload variables passed across extraction pipeline."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    correlation_id: str = Field(min_length=1)
    rule_engine_config: Mapping[str, Any] = Field(default_factory=dict)
    environment: str = Field(default="production", min_length=1)
    metadata: Mapping[str, Any] = Field(default_factory=dict)


class FeatureCollection(BaseModel):
    """Official aggregate output DTO of Book 04."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    features: tuple[Feature, ...] = Field(default_factory=tuple)
    statistics: FeatureEngineeringStatistics
    context: FeatureExtractionContext


class ValidationErrorDetail(BaseModel):
    """Detailed record of a failed canonical feature validation rule."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    feature_id: str | None = None
    field: str | None = None
    message: str = Field(min_length=1)
    error_type: str = Field(min_length=1)


class ValidationWarningDetail(BaseModel):
    """Detailed record of an audit warning during feature validation."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    feature_id: str | None = None
    field: str | None = None
    message: str = Field(min_length=1)
    warning_type: str = Field(min_length=1)


class ValidationSummary(BaseModel):
    """Immutable audit summary generated during feature validation runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    status: str = Field(min_length=1)  # e.g., "VALID", "WARNING", "INVALID"
    errors: tuple[ValidationErrorDetail, ...] = Field(default_factory=tuple)
    warnings: tuple[ValidationWarningDetail, ...] = Field(default_factory=tuple)
    duplicate_count: int = Field(default=0, ge=0)
    validation_timestamp: str = Field(min_length=1)
    rules_version: str = Field(min_length=1)


class FeatureStatistics(BaseModel):
    """Performance and distribution stats compiled for the canonical collection."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_feature_count: int = Field(default=0, ge=0)
    duplicate_count: int = Field(default=0, ge=0)
    validation_error_count: int = Field(default=0, ge=0)
    warning_count: int = Field(default=0, ge=0)
    category_counts: Mapping[str, int] = Field(default_factory=dict)


class CanonicalFeatureCollection(BaseModel):
    """Consolidated aggregate payload holding verified features from all domains."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    skills: FeatureCollection
    experience: FeatureCollection
    education: FeatureCollection
    projects: FeatureCollection
    certifications: FeatureCollection
    statistics: FeatureStatistics
    validation_summary: ValidationSummary
    metadata: Mapping[str, Any] = Field(default_factory=dict)

