"""ScoringContext model definition.

Purpose:
    Define frozen context holding the CanonicalMatchCollection and ScoringRules.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from typing import Any
from ats_engine.domain.matching.models import CanonicalMatchCollection


class ScoringContext(BaseModel):
    """Immutable scoring pipeline context DTO."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    match_collection: CanonicalMatchCollection
    rules: Any
