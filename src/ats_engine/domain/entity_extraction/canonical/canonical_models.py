"""Models representing the Canonical Entity Collection and Validation Summary.

Purpose:
    Define immutable data schemas holding the aggregated collection of entities,
    structural validation messages, and extraction statistics.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.entity_extraction.models import EntityCollection
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceCollection
from ats_engine.domain.entity_extraction.education.education_models import EducationCollection
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.certification.certification_models import CertificationCollection


class ValidationErrorDetail(BaseModel):
    """Immutable detail representing a single validation issue."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entity_id: str
    entity_type: str
    field_name: str
    error_message: str
    severity: str = "ERROR"  # "ERROR" or "WARNING"


class ValidationSummary(BaseModel):
    """Immutable summary containing all structural and cross-reference validation reports."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    status: str  # "VALID" or "INVALID"
    errors: tuple[ValidationErrorDetail, ...] = Field(default_factory=tuple)
    warnings: tuple[ValidationErrorDetail, ...] = Field(default_factory=tuple)
    duplicate_count: int = Field(default=0, ge=0)
    reference_errors: int = Field(default=0, ge=0)
    validation_timestamp: str = Field(min_length=1)
    rules_version: str = Field(min_length=1)


class EntityStatistics(BaseModel):
    """Immutable execution statistics aggregated across all extraction modules."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    contact_count: int = Field(ge=0)
    skill_count: int = Field(ge=0)
    experience_count: int = Field(ge=0)
    education_count: int = Field(ge=0)
    project_count: int = Field(ge=0)
    certification_count: int = Field(ge=0)
    duplicate_count: int = Field(ge=0)
    validation_error_count: int = Field(ge=0)
    processing_duration_seconds: float = Field(ge=0.0)


class CanonicalEntityCollection(BaseModel):
    """The consolidated immutable contract and final output of Book 03."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    contacts: EntityCollection
    skills: SkillCollection
    experiences: ExperienceCollection
    education: EducationCollection
    projects: ProjectCollection
    certifications: CertificationCollection
    validation_summary: ValidationSummary
    statistics: EntityStatistics
