"""Pydantic v2 models representing the immutable document structures.

Purpose:
    Provide type-safe, validated, and frozen data schemas for parsed and normalized documents.
"""

from __future__ import annotations

from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class RawDocument(BaseModel):
    """Immutable representation of raw extracted document contents."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    filename: str = Field(min_length=1)
    file_size_bytes: int = Field(ge=0)
    raw_content: str
    pages: tuple[str, ...] = ()


class NormalizedDocument(BaseModel):
    """Immutable representation of normalized and clean text content."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    cleaned_content: str
    paragraph_count: int = Field(ge=0)
    line_count: int = Field(ge=0)
    char_count: int = Field(ge=0)


class DocumentMetadata(BaseModel):
    """Immutable generic infrastructure and parsing execution metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    file_size_bytes: int = Field(ge=0)
    page_count: int = Field(ge=0)
    character_count: int = Field(ge=0)
    line_count: int = Field(ge=0)
    paragraph_count: int = Field(ge=0)
    extraction_duration_seconds: float = Field(ge=0.0)
    parser_used: str = Field(min_length=1)
    encoding: str = Field(min_length=1)


class ParsingResult(BaseModel):
    """Unified container representing the complete output of a document parse operation."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    raw_document: RawDocument
    normalized_document: NormalizedDocument
    metadata: DocumentMetadata
