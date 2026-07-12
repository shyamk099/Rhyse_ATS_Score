"""Models representing the physical document structure.

Purpose:
    Define immutable representations of physical lines, blocks, and layout map.
"""

from __future__ import annotations

from enum import Enum
from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class BlockType(str, Enum):
    """Supported physical layout block categories."""

    TEXT = "TEXT"
    HEADING = "HEADING"
    LIST = "LIST"
    TABLE = "TABLE"
    UNKNOWN = "UNKNOWN"


class PhysicalLine(BaseModel):
    """Immutable representation of a single extracted line and its physical metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    text: str
    line_number: int = Field(ge=1)
    page_number: int = Field(ge=1)
    indentation_spaces: int = Field(ge=0)
    character_count: int = Field(ge=0)


class PhysicalBlock(BaseModel):
    """Immutable collection of physical lines sharing layout properties."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    block_type: BlockType
    lines: tuple[PhysicalLine, ...]
    raw_text: str


class DocumentLayout(BaseModel):
    """Immutable map representing the sequential physical reading order of the document."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    blocks: tuple[PhysicalBlock, ...]
    total_blocks: int = Field(ge=0)
    total_lines: int = Field(ge=0)
