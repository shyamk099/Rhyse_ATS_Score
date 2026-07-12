"""Pydantic model representing contact candidates during validation and cleaning stages.

Purpose:
    Provide an intermediate mutable/immutable structure to store pattern matches.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ContactCandidate(BaseModel):
    """Candidate match holding details extracted via regular expressions."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    value: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
