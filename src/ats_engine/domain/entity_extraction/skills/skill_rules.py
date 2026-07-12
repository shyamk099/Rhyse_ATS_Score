"""Pydantic schemas representing configurable skill extraction rules.

Purpose:
    Define configuration schemas for skill definitions, aliases, synonyms,
    canonical IDs, scopes, and priorities loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class SkillDefinition(BaseModel):
    """Immutable representation of a canonical skill in the skills taxonomy."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    aliases: Sequence[str] = Field(default_factory=list)
    synonyms: Sequence[str] = Field(default_factory=list)
    category: str = Field(default="technical")


class SkillExtractionRules(BaseModel):
    """Configuration rules governing dictionary matchers and resolver behaviors."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    dictionary: Mapping[str, SkillDefinition] = Field(
        default={
            "SKILL-001": SkillDefinition(
                name="Python", aliases=["py", "python3"], category="programming_language"
            ),
            "SKILL-002": SkillDefinition(
                name="C#", aliases=["c sharp", "csharp"], category="programming_language"
            ),
            "SKILL-003": SkillDefinition(
                name="JavaScript", aliases=["js", "es6"], category="programming_language"
            ),
            "SKILL-004": SkillDefinition(
                name="Node.js", aliases=["nodejs", "node js"], category="runtime"
            ),
            "SKILL-005": SkillDefinition(name="Java", category="programming_language"),
        }
    )

    confidence_mappings: Mapping[str, float] = Field(
        default={
            "SKILLS": 1.0,
            "EXPERIENCE": 0.8,
            "DEFAULT": 0.6,
        }
    )

    extraction_scope: Sequence[str] = Field(default=("SKILLS",))
    duplicate_strategy: str = Field(default="KEEP_HIGHEST_CONFIDENCE")  # KEEP_FIRST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL
    overlap_strategy: str = Field(default="LONGEST_MATCH")  # LONGEST_MATCH
    default_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
