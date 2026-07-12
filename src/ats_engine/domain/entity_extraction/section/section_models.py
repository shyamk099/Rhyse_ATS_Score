"""Models representing document sections and boundaries.

Purpose:
    Define immutable representations of section components, collections,
    and metadata stats.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.document_processing.segmentation_models import DocumentSegment


class SectionCandidate(BaseModel):
    """Immutable match details for identified section headings."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    block_index: int = Field(ge=0)
    matched_text: str = Field(min_length=1)
    section_type: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = Field(min_length=1)


class SectionMetadata(BaseModel):
    """Immutable physical properties tracking the bounds of a segment section range."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    section_type: str = Field(min_length=1)
    page_range: tuple[int, int]
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_reason: str = Field(min_length=1)


class Section(BaseModel):
    """Immutable section containing logical boundaries and segment collections."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    section_type: str = Field(min_length=1)
    text_content: str
    metadata: SectionMetadata
    associated_segments: tuple[DocumentSegment, ...]


class SectionDetectionStatistics(BaseModel):
    """Immutable execution statistics for section detection runs."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    section_counts: Mapping[str, int] = Field(default_factory=dict)
    total_sections: int = Field(ge=0)
    execution_duration_seconds: float = Field(ge=0.0)


class SectionCollection(BaseModel):
    """Immutable aggregation contract containing all logical sections in reading order."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    sections: tuple[Section, ...]
    statistics: SectionDetectionStatistics
