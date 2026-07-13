"""Models representing certification candidates, assembled records, and collections.

Purpose:
    Define immutable data schemas holding compound certification fields,
    provenance references, and extraction statistics.
    Follows the standardized compound entity lifecycle:
    Candidate → Normalized → Assembled → Entity → Collection.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class CertificationURL(BaseModel):
    """Immutable representation of a Credential URL preserving provenance."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    original_value: str = Field(min_length=1)
    normalized_value: str = Field(min_length=1)
    matched_rule: str = Field(min_length=1)


class CertificationCandidate(BaseModel):
    """Intermediate candidate holding raw evidence matches from segment text."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    section_type: str = Field(min_length=1)
    raw_text: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    detected_dates: tuple[str, ...] = Field(default_factory=tuple)
    detected_name: str | None = None
    detected_issuer: str | None = None
    detected_credential_id: str | None = None
    detected_credential_url: str | None = None


class NormalizedCertification(BaseModel):
    """Normalized intermediate certification carrying cleaned field values."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    candidate: CertificationCandidate
    certification_name: str | None = None
    issuing_organization: str | None = None
    credential_id_raw: str | None = None
    credential_url: CertificationURL | None = None
    issue_date_raw: str | None = None
    expiration_date_raw: str | None = None
    validity_status_raw: str | None = None


class AssembledCertification(BaseModel):
    """Compound certification record grouping all evidence into one immutable aggregate."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    certification_id: str = Field(min_length=1)
    certification_name: str | None = None
    issuing_organization: str | None = None
    credential_id_raw: str | None = None
    credential_url: CertificationURL | None = None
    issue_date_raw: str | None = None
    expiration_date_raw: str | None = None
    validity_status_raw: str | None = None
    associated_skill_ids: tuple[str, ...] = Field(default_factory=tuple)
    associated_skills_raw: tuple[str, ...] = Field(default_factory=tuple)
    description_raw: str | None = None
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class CertificationEntity(BaseModel):
    """Final immutable compound certification entity with full provenance metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    certification_id: str = Field(min_length=1)
    certification_name: str | None = None
    issuing_organization: str | None = None
    credential_id_raw: str | None = None
    credential_url: CertificationURL | None = None
    issue_date_raw: str | None = None
    expiration_date_raw: str | None = None
    validity_status_raw: str | None = None
    associated_skill_ids: tuple[str, ...] = Field(default_factory=tuple)
    associated_skills_raw: tuple[str, ...] = Field(default_factory=tuple)
    description_raw: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = ""
    matched_rules: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_text: str = ""


class CertificationExtractionStatistics(BaseModel):
    """Immutable execution statistics for certification extraction runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_certifications: int = Field(ge=0)
    active_certifications: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class CertificationCollection(BaseModel):
    """Immutable aggregation contract containing all extracted certification records."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[CertificationEntity, ...]
    statistics: CertificationExtractionStatistics
