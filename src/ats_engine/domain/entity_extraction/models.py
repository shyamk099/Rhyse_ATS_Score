"""Pydantic v2 models representing entity extraction data contracts.

Purpose:
    Define immutable data structures for extracted entities, collections,
    statistics, and read-only execution context.
"""

from __future__ import annotations

from typing import Any, Mapping
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument


class EntityLocation(BaseModel):
    """Immutable coordinates indicating the physical segment offset of the entity."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)


class ExtractedEntity(BaseModel):
    """Immutable representation of a generic extracted entity."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entity_type: str = Field(min_length=1)
    value: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    location: EntityLocation
    metadata: Mapping[str, str] = Field(default_factory=dict)


class EntityExtractionStatistics(BaseModel):
    """Immutable extraction execution metrics."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    extractor_counts: Mapping[str, int] = Field(default_factory=dict)
    total_entities: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class EntityCollection(BaseModel):
    """Immutable aggregation contract containing all extracted entities and stats."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    entities: tuple[ExtractedEntity, ...]
    statistics: EntityExtractionStatistics


class EntityExtractionContext(BaseModel):
    """Read-only context containing configuration and correlation identifiers for execution."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    canonical_document: CanonicalDocument
    correlation_id: str = Field(min_length=1)
    rule_engine_config: Mapping[str, Any] = Field(default_factory=dict)
