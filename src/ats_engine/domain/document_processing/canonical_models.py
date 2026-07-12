"""Pydantic v2 models representing the immutable CanonicalDocument.

Purpose:
    Define the final verified schema contract for Book 02 (Document Processing).
    This model acts strictly as a data transfer contract and must not contain logic.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection


class CanonicalMetadata(BaseModel):
    """Immutable metadata summarizing the source document characteristics."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    canonical_id: str = Field(min_length=1)
    source_filename: str = Field(min_length=1)
    file_size_bytes: int = Field(ge=0)
    page_count: int = Field(ge=1)
    parser_used: str = Field(min_length=1)
    encoding: str = Field(min_length=1)


class CanonicalStatistics(BaseModel):
    """Immutable aggregated structural counts for validation verification."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    total_characters: int = Field(ge=0)
    total_lines: int = Field(ge=0)
    total_paragraphs: int = Field(ge=0)
    total_segments: int = Field(ge=0)
    total_blocks: int = Field(ge=0)


class CanonicalDocument(BaseModel):
    """The final verified, immutable data transfer contract representing the canonical parsed document."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    canonical_id: str = Field(min_length=1)
    normalized_document: NormalizedDocument
    document_layout: DocumentLayout
    segment_collection: SegmentCollection
    metadata: CanonicalMetadata
    statistics: CanonicalStatistics
