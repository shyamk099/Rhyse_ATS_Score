"""Models representing skill candidates, normalized instances, and collections.

Purpose:
    Define immutable data schemas holding offsets, canonical details,
    provenance details, and extraction statistics.
"""

from __future__ import annotations

from typing import Mapping
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.entity_extraction.models import ExtractedEntity


class SkillCandidate(BaseModel):
    """Intermediate candidate matching a taxonomy entry before validation or normalization."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    matched_text: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    skill_id: str = Field(min_length=1)
    match_type: str = Field(min_length=1)  # "direct", "alias", "synonym"
    match_term: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    section_type: str = Field(min_length=1)


class NormalizedSkill(BaseModel):
    """Immutable normalized representation carrying full extraction provenance."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    candidate: SkillCandidate
    skill_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    matched_token: str = Field(min_length=1)
    normalized_token: str = Field(min_length=1)
    dictionary_entry: str = Field(min_length=1)
    alias_matched: str | None = None
    synonym_matched: str | None = None


class SkillExtractionStatistics(BaseModel):
    """Immutable execution statistics for skill extraction runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_skills_found: int = Field(ge=0)
    unique_skills_count: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class SkillCollection(BaseModel):
    """Immutable aggregation contract containing all extracted skills and stats."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[ExtractedEntity, ...]
    statistics: SkillExtractionStatistics
