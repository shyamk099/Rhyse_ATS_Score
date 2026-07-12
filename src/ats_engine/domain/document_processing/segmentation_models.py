"""Models representing the document segmentation results.

Purpose:
    Define immutable representations of document segments and their collections.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.document_processing.structure_models import PhysicalBlock


class SegmentMetadata(BaseModel):
    """Immutable metadata tracking physical limits and locations of a segment."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    reading_order: int = Field(ge=1)
    page_range: tuple[int, int]
    block_range: tuple[int, int]
    character_count: int = Field(ge=0)
    line_count: int = Field(ge=0)


class DocumentSegment(BaseModel):
    """Immutable structural segment containing raw lines and associated physical blocks."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segment_id: str = Field(min_length=1)
    text_content: str
    metadata: SegmentMetadata
    associated_blocks: tuple[PhysicalBlock, ...]


class SegmentCollection(BaseModel):
    """Immutable collection of all physical document segments in reading order."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    segments: tuple[DocumentSegment, ...]
    total_segments: int = Field(ge=0)
    total_characters: int = Field(ge=0)
